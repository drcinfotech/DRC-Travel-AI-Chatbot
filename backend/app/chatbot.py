"""
Travel & Hospitality chatbot engine.

Flow:
  1. Safety check first — booking fraud / travel advisory / visa consult /
     payment / social engineering all short-circuit with a refusal block.
  2. Otherwise, classify intent.
  3. Dispatch to handler.
"""
from __future__ import annotations

from .catalog import catalog
from .intents import Classification, classify
from .safety import (
    check_safety,
    build_booking_fraud_block,
    build_travel_advisory_block,
    build_visa_consult_block,
    build_payment_privacy_block,
    build_social_engineering_block,
)
from .sessions import Session


# ─── Block helpers ─────────────────────────────────────────
def _text(content: str) -> dict:
    return {"type": "text", "content": content}


def _disclaimer(content: str) -> dict:
    return {"type": "disclaimer", "content": content}


# ─── Curated day-by-day itineraries (fictional) ────────────
ITINERARY_TEMPLATES = {
    "Goa": [
        {"day": 1, "title": "North Goa arrival", "activities": [
            "Arrive Goa, transfer to hotel in Calangute",
            "Lunch at a beach shack",
            "Sunset at Baga Beach",
            "Dinner at a fish-curry-rice spot in Calangute",
        ]},
        {"day": 2, "title": "Beaches & churches", "activities": [
            "Anjuna flea market (Wednesdays only)",
            "Lunch at a hilltop café in Vagator",
            "Basilica of Bom Jesus & Old Goa churches",
            "Sunset cruise on the Mandovi",
        ]},
        {"day": 3, "title": "Dudhsagar day trip", "activities": [
            "Early start for Dudhsagar Falls jeep safari",
            "Spice plantation tour with traditional lunch",
            "Return for evening at the hotel pool",
        ]},
        {"day": 4, "title": "South Goa & relax", "activities": [
            "Drive south to Palolem & Agonda",
            "Beach time at quieter southern stretches",
            "Lunch with local feni tasting (optional)",
            "Return north for last-night dinner",
        ]},
        {"day": 5, "title": "Departure", "activities": [
            "Last beach walk + breakfast",
            "Souvenir shopping in Calangute",
            "Transfer to airport for departure",
        ]},
    ],
    "Manali": [
        {"day": 1, "title": "Arrival in the hills", "activities": [
            "Arrive at hotel, check in & rest",
            "Walk through Old Manali for cafés & boutiques",
            "Dinner with bonfire at the hotel",
        ]},
        {"day": 2, "title": "Local sightseeing", "activities": [
            "Hidimba Devi Temple in cedar forest",
            "Manu Temple & Vashisht hot springs",
            "Mall Road afternoon",
            "Dinner at a riverside restaurant",
        ]},
        {"day": 3, "title": "Solang Valley", "activities": [
            "Day trip to Solang Valley",
            "Optional: paragliding, snow activities (in season)",
            "Lunch on-site",
            "Evening back in town",
        ]},
        {"day": 4, "title": "Rohtang or Kullu", "activities": [
            "If open: Rohtang Pass excursion (snow point)",
            "Otherwise: Kullu Valley + Naggar Castle",
            "Apple-orchard visit (in season)",
        ]},
        {"day": 5, "title": "Adventure day", "activities": [
            "River rafting in Beas (in season)",
            "Jogini Falls trek (moderate, half day)",
            "Free evening for shopping",
        ]},
        {"day": 6, "title": "Departure", "activities": [
            "Breakfast, late check-out",
            "Last cup of café coffee in Old Manali",
            "Volvo / cab to Delhi",
        ]},
    ],
    "Jaisalmer": [
        {"day": 1, "title": "Arrival in the Golden City", "activities": [
            "Arrive, check in to a haveli or fort hotel",
            "Sunset at Bada Bagh cenotaphs",
            "Dinner with Rajasthani folk music",
        ]},
        {"day": 2, "title": "Fort & havelis", "activities": [
            "Jaisalmer Fort walking tour (still inhabited)",
            "Patwon Ki Haveli — most ornate of the lot",
            "Lunch at a rooftop café with fort views",
            "Gadisar Lake at sunset",
        ]},
        {"day": 3, "title": "Sam Sand Dunes overnight", "activities": [
            "Drive to Sam (~40 km west)",
            "Camel safari at sunset",
            "Dinner & cultural show at the tented camp",
            "Stargazing & overnight in luxury tent",
        ]},
    ],
    "Dubai": [
        {"day": 1, "title": "Arrival & Marina", "activities": [
            "Arrive at DXB, transfer to Marina hotel",
            "Marina Walk in the evening",
            "Dinner at JBR Beach with skyline views",
        ]},
        {"day": 2, "title": "Old Dubai", "activities": [
            "Dubai Museum (Al Fahidi Fort)",
            "Abra boat across the Creek to Deira",
            "Spice & Gold Souks",
            "Evening at Dubai Frame",
        ]},
        {"day": 3, "title": "Modern marvels", "activities": [
            "Burj Khalifa 124th floor (book At The Top tickets)",
            "Dubai Mall + aquarium + ice rink",
            "Dubai Fountain show in the evening",
            "Dinner inside the mall",
        ]},
        {"day": 4, "title": "Desert safari", "activities": [
            "Free morning at the hotel pool",
            "Desert safari pickup at 3 PM",
            "Dune bashing + camel ride + henna + BBQ dinner",
            "Late return to hotel",
        ]},
        {"day": 5, "title": "Atlantis / Palm", "activities": [
            "Monorail to Palm Jumeirah",
            "Atlantis Aquaventure (full day) or Lost Chambers",
            "Late lunch at one of the Palm restaurants",
            "Return to hotel",
        ]},
        {"day": 6, "title": "Departure", "activities": [
            "Souvenir shopping at Karama or Naif",
            "Brunch (Dubai is famous for these)",
            "Transfer to DXB for departure",
        ]},
    ],
}


# ─── Intent handlers ───────────────────────────────────────
def _handle_greeting(_s: Session):
    return [
        _text(
            "Hi 👋 — I'm your Trip Assistant. I can help you search flights, find hotels, "
            "explore destinations, build a day-by-day itinerary, check visa requirements, "
            "and manage your bookings. Where would you like to go?"
        )
    ], ["Flights Mumbai to Delhi", "Hotels in Goa", "Show packages", "Build me an itinerary"]


def _handle_goodbye(_s: Session):
    return [_text("Safe travels. Come back when the wanderlust hits.")], []


def _handle_thanks(_s: Session):
    return [_text("Happy to help. Anything else for the trip?")], \
           ["My bookings", "Build itinerary", "Weather forecast"]


def _handle_search_flights(c: Classification, _s: Session):
    cities = c.entities["cities"]
    flights = catalog.flights()

    origin = cities.get("from")
    dest   = cities.get("to")
    if not origin and not dest and cities.get("all"):
        # Fall back: if we found exactly 2 plain cities, treat as from→to
        if len(cities["all"]) >= 2:
            origin, dest = cities["all"][0], cities["all"][1]

    filtered = flights
    if origin: filtered = [f for f in filtered if f["from"]["city"] == origin]
    if dest:   filtered = [f for f in filtered if f["to"]["city"] == dest]

    if not filtered:
        return [_text(
            "I couldn't find flights matching that route in this demo's catalog. "
            "Try Mumbai → Delhi, Mumbai → Goa, or Delhi → Dubai — those are in scope."
        )], ["Mumbai to Delhi", "Mumbai to Goa", "Delhi to Dubai"]

    return [
        _text(f"I found **{len(filtered)} flights** matching your search:"),
        {
            "type": "flight_list",
            "title": "Available flights",
            "route": {"from": origin, "to": dest, "date": filtered[0]["date"] if filtered else None},
            "items": filtered,
            "total": len(filtered),
        },
    ], ["Show flight details", "Cheapest first", "Book this flight", "Add hotel too"]


def _handle_flight_detail(c: Classification, s: Session):
    fid = c.entities.get("flight_id") or s.last_flight_id
    if not fid:
        return [_text("Which flight? You can paste a flight ID (like FL-7821) or run a search first.")], \
               ["Search flights", "Mumbai to Delhi"]
    f = catalog.flight(fid)
    if not f:
        return [_text(f"I couldn't find flight **{fid}**.")], []
    s.last_flight_id = fid
    return [
        _text(f"Here are the details for **{f['airline']} {f['flight_number']}**:"),
        {"type": "flight_detail", "flight": f},
    ], ["Book this flight", "Compare with others", "Check baggage rules"]


def _handle_search_hotels(c: Classification, s: Session):
    hotels = catalog.hotels()
    city = c.entities["cities"].get("to") or (c.entities["cities"].get("all") or [None])[0]
    if city:
        hotels = [h for h in hotels if h["city"] == city]
    if not hotels:
        return [_text(
            f"I couldn't find hotels in {city or 'that city'} in this demo's catalog. "
            "Try Goa, Manali, Jaisalmer, Mumbai, or Dubai."
        )], ["Hotels in Goa", "Hotels in Manali", "Hotels in Dubai"]
    if city:
        s.last_destination = city
    return [
        _text(f"I found **{len(hotels)} hotels** in {city or 'this demo'}:"),
        {"type": "hotel_list", "title": f"Hotels{' in ' + city if city else ''}", "items": hotels, "total": len(hotels)},
    ], ["Show top-rated first", "Book this hotel", "Add flight too", "Build itinerary"]


def _handle_hotel_detail(c: Classification, s: Session):
    hid = c.entities.get("hotel_id") or s.last_hotel_id
    if not hid:
        return [_text("Which hotel? Paste a hotel ID (like HT-3301) or run a search first.")], \
               ["Search hotels", "Hotels in Goa"]
    h = catalog.hotel(hid)
    if not h:
        return [_text(f"I couldn't find hotel **{hid}**.")], []
    s.last_hotel_id = hid
    return [
        _text(f"Here are the details for **{h['name']}**:"),
        {"type": "hotel_detail", "hotel": h},
    ], ["Book this hotel", "Add flights", "Compare with similar"]


def _handle_view_packages(_c: Classification, _s: Session):
    items = catalog.packages()
    return [
        _text(f"Here are **{len(items)} curated packages** that bundle flights + stay + sightseeing:"),
        {"type": "package", "title": "Curated packages", "items": items},
        _disclaimer(
            "Package prices are 'starting from' and vary by date, group size, and room category. "
            "Final pricing locks at checkout based on real-time availability."
        ),
    ], ["Book a package", "Customise dates", "Build my own"]


def _handle_destinations(c: Classification, s: Session):
    cities = c.entities["cities"].get("all") or []
    if cities:
        dest = catalog.destination(cities[0])
        if dest:
            s.last_destination = dest["name"]
            return [
                _text(f"Here's an overview of **{dest['name']}**:"),
                {"type": "destination", "items": [dest]},
            ], [f"Build {dest['name']} itinerary", f"Hotels in {dest['name']}", "Weather forecast", "Visa info"]

    items = catalog.destinations()
    return [
        _text(f"Here are **{len(items)} destinations** in this demo's catalog:"),
        {"type": "destination", "items": items},
    ], ["Goa", "Manali", "Jaisalmer", "Dubai"]


def _handle_build_itinerary(c: Classification, s: Session):
    cities = c.entities["cities"].get("all") or []
    dest = cities[0] if cities else s.last_destination
    if not dest:
        return [_text(
            "Which destination would you like an itinerary for? I have curated day-by-day plans for "
            "**Goa, Manali, Jaisalmer, and Dubai** in this demo."
        )], ["Goa itinerary", "Manali itinerary", "Jaisalmer itinerary", "Dubai itinerary"]

    s.last_destination = dest
    template = ITINERARY_TEMPLATES.get(dest)
    if not template:
        return [_text(
            f"I don't have a curated itinerary for **{dest}** in this demo. Try Goa, Manali, Jaisalmer, or Dubai."
        )], ["Goa", "Manali", "Jaisalmer", "Dubai"]

    # If user requested specific number of days, slice template
    days = c.entities.get("days")
    if days and days < len(template):
        plan = template[:days]
    else:
        plan = template
    nights = len(plan) - 1
    return [
        _text(f"Here's a **{len(plan)}-day / {nights}-night itinerary for {dest}**:"),
        {
            "type": "itinerary",
            "destination": dest,
            "nights": nights,
            "days": len(plan),
            "day_plan": plan,
            "note": "Itinerary is illustrative — actual timing may shift with weather, transport, and on-site availability.",
        },
    ], [f"Hotels in {dest}", f"Flights to {dest}", "Customise itinerary", "Package deal"]


def _handle_view_bookings(_c: Classification, _s: Session):
    items = catalog.bookings()
    return [
        _text(f"You have **{len(items)} active bookings**:"),
        {"type": "bookings", "items": items},
    ], ["Web check-in", "Cancel a booking", "Build itinerary"]


def _handle_booking_detail(c: Classification, _s: Session):
    bid = c.entities.get("booking_id")
    if not bid:
        return [_text("Which booking would you like to view?")], ["My bookings"]
    b = catalog.booking(bid)
    if not b:
        return [_text(f"I couldn't find booking **{bid}**.")], []
    return [
        _text(f"Here are the details for booking **{bid}**:"),
        {"type": "booking_confirmation", "booking": b},
    ], ["Web check-in", "Cancel this booking", "Modify dates"]


def _handle_checkin(_c: Classification, _s: Session):
    flights = catalog.flights()
    f = flights[0]   # first match for demo
    return [
        _text("Web check-in is open for your upcoming flight. Here's a sample boarding pass:"),
        {
            "type": "check_in",
            "booking_id": "BK-44102",
            "flight": {
                "airline": f["airline"], "flight_number": f["flight_number"],
                "from": f["from"], "to": f["to"],
                "depart": f["depart"], "arrive": f["arrive"], "date": f["date"], "gate": "G14",
            },
            "passenger": {"name": "MR DEMO TRAVELER", "type": "Adult", "category": "ECONOMY"},
            "seat": "14A",
            "boarding_pass_ready": True,
        },
        _disclaimer(
            "Boarding pass is illustrative. In a real platform, this would be a scannable QR/PDF "
            "tied to your verified identity and booking record."
        ),
    ], ["Download PDF", "Choose another seat", "Add bags"]


def _handle_weather(c: Classification, s: Session):
    cities = c.entities["cities"].get("all") or []
    dest = cities[0] if cities else s.last_destination
    if not dest:
        return [_text(
            "Which destination's weather would you like? Try *'weather in Goa'* or *'weather forecast for Dubai'*."
        )], ["Weather in Goa", "Weather in Manali", "Weather in Dubai"]

    s.last_destination = dest

    # Demo weather — fictional, illustrative
    forecasts = {
        "Goa":       [("Dec 12", 31, 23, "Sunny"),      ("Dec 13", 30, 22, "Partly cloudy"),
                      ("Dec 14", 29, 23, "Sunny"),      ("Dec 15", 30, 22, "Light breeze")],
        "Manali":    [("Dec 12", 8,  -2, "Snow showers"),("Dec 13", 7, -3, "Snow"),
                      ("Dec 14", 9, -1, "Partly sunny"), ("Dec 15", 10, 0, "Sunny")],
        "Jaisalmer": [("Dec 12", 24, 10, "Sunny"),     ("Dec 13", 25, 11, "Clear"),
                      ("Dec 14", 24, 10, "Sunny"),     ("Dec 15", 23, 9,  "Cold night")],
        "Dubai":     [("Dec 12", 27, 18, "Sunny"),     ("Dec 13", 28, 19, "Clear"),
                      ("Dec 14", 28, 19, "Sunny"),     ("Dec 15", 26, 18, "Slightly windy")],
        "Mumbai":    [("Dec 12", 32, 22, "Hazy"),      ("Dec 13", 32, 22, "Sunny"),
                      ("Dec 14", 31, 22, "Partly cloudy"),("Dec 15", 31, 23, "Sunny")],
    }
    forecast = forecasts.get(dest)
    if not forecast:
        return [_text(
            f"I don't have a forecast loaded for **{dest}** in this demo. Try Goa, Manali, Jaisalmer, Dubai, or Mumbai."
        )], ["Weather in Goa", "Weather in Dubai"]

    return [
        _text(f"Here's the **4-day forecast for {dest}**:"),
        {
            "type": "weather",
            "destination": dest,
            "forecast": [{"date": d, "high": hi, "low": lo, "conditions": c} for (d, hi, lo, c) in forecast],
            "note": "Illustrative demo data. In a real platform, this would pull from a weather provider (OpenWeather, Tomorrow.io, IMD, etc.) for live forecasts."
        },
    ], ["What to pack", f"Hotels in {dest}", "Build itinerary"]


def _handle_visa_info(c: Classification, s: Session):
    cities = c.entities["cities"].get("all") or []
    dest = cities[0] if cities else s.last_destination
    if not dest:
        return [_text(
            "Which destination's visa info would you like? Try *'visa for Dubai'* — I have general info on UAE here. "
            "For other countries, I'll point you at the embassy."
        )], ["Visa for Dubai", "Visa for Goa", "Domestic destinations"]

    s.last_destination = dest
    dest_obj = catalog.destination(dest)

    if not dest_obj:
        return [_text(f"I don't have visa details on **{dest}** in this demo.")], ["Destinations"]

    if dest_obj["country"] == "India":
        return [
            _text(f"**{dest}** is a domestic destination — Indian citizens don't need a visa to travel within India."),
            _disclaimer("Foreign nationals visiting India need a visa — check the e-Visa portal at indianvisaonline.gov.in"),
        ], ["Build itinerary", f"Hotels in {dest}", "Flights"]

    # Demo: only Dubai has a real visa flow loaded
    docs = [
        {"name": "Valid passport (6+ months validity)",       "category": "Identity", "required": True,
         "note": "At least 2 blank pages required"},
        {"name": "Passport-size photographs",                  "category": "Identity", "required": True,
         "note": "White background · UAE specs slightly different from Indian standards"},
        {"name": "Confirmed return air ticket",                "category": "Travel",   "required": True,
         "note": "Round-trip booking confirmation"},
        {"name": "Hotel booking confirmation",                 "category": "Travel",   "required": True,
         "note": "For the entire duration of your stay"},
        {"name": "Bank statement (last 3 months)",             "category": "Financial","required": True,
         "note": "Shows financial standing; min balance varies by visa duration"},
        {"name": "Travel insurance",                           "category": "Travel",   "required": False,
         "note": "Strongly recommended for UAE; some visa categories require it"},
        {"name": "Visa fee payment receipt",                    "category": "Process",  "required": True,
         "note": "Pay through authorized agent or via UAE GDRFA portal"},
    ]
    return [
        _text(f"General visa info for **{dest}** (UAE):"),
        {
            "type": "visa",
            "destination": dest,
            "country": dest_obj["country"],
            "summary": dest_obj["visa_note"],
            "documents": docs,
            "note": "This is general guidance, not personalized advice. Final requirements depend on your nationality, passport, recent travel history, and visa duration. Always confirm with the UAE embassy or an authorized travel agent before applying."
        },
    ], ["Apply through travel agent", "Embassy contact", "Package with visa"]


def _handle_cancel_modify(_c: Classification, _s: Session):
    return [_text(
        "Cancellation and modification policies depend on the booking and the airline/hotel. Here's the gist for this demo:"
    ), _disclaimer(
        "• Refundable flight: full refund per fare rules (small ticketing fee may apply)\n"
        "• Non-refundable flight: cancellation charge per fare class; some carriers allow rebooking with fee\n"
        "• Hotels: free cancellation windows vary (24 hr / 48 hr / 7 days) — see the cancellation line on the hotel detail card\n"
        "• Packages: terms vary; usually a sliding-scale cancellation fee\n\n"
        "In a production app, this handler would query the actual booking and surface the live policy."
    )], ["My bookings", "Modify dates instead", "Contact support"]


def _handle_loyalty(_c: Classification, _s: Session):
    return [
        _text(
            "Loyalty programs are airline-specific. In this demo:\n"
            "• **Skyline Air — SkyMiles**: 1 mile per ₹4 spent · redeem from 10,000 miles\n"
            "• **Northbound — Compass Club**: tier-based earn · status-match available\n"
            "• **Coastline Express**: doesn't have a loyalty program yet"
        ),
        _disclaimer(
            "Real loyalty programs have detailed earn/burn tables, expiry policies, and partner networks. "
            "In a production app, this would pull your live balance and recent transactions."
        ),
    ], ["My bookings", "Earn miles next trip", "Tier benefits"]


def _handle_contact_support(_c: Classification, _s: Session):
    return [_text(
        "Sure — for issues with a confirmed booking (refunds, schedule changes, missed connections, lost baggage), "
        "support is the right place. In this demo, support isn't connected to a real ticket system. In a real "
        "app, this would open a chat with a human agent or create a support ticket."
    )], ["My bookings", "Cancellation policy", "Web check-in"]


def _handle_unknown(_c: Classification, _s: Session):
    return [_text(
        "I'm not sure I caught that. I can search flights and hotels, show packages, build itineraries, "
        "check visa info and weather, or manage your bookings. Try one of the buttons below."
    )], ["Search flights", "Search hotels", "Show packages", "Build itinerary"]


# ─── Engine ────────────────────────────────────────────────
class ChatbotEngine:
    def respond(self, message: str, session: Session) -> dict:
        safety = check_safety(message)
        if safety.flag == "social_engineering":
            return self._safety_response(session, "social_engineering",
                build_social_engineering_block(),
                ["Search flights", "Search hotels", "My bookings"])
        if safety.flag == "payment_privacy":
            return self._safety_response(session, "payment_privacy",
                build_payment_privacy_block(),
                ["Go to checkout", "My bookings", "Cancellation policy"])
        if safety.flag == "booking_fraud":
            return self._safety_response(session, "booking_fraud",
                build_booking_fraud_block(),
                ["My bookings", "Search flights", "Contact support"])
        if safety.flag == "visa_consult":
            return self._safety_response(session, "visa_consult",
                build_visa_consult_block(),
                ["General visa info", "Embassy contact", "Travel insurance"])
        if safety.flag == "travel_advisory":
            return self._safety_response(session, "travel_advisory",
                build_travel_advisory_block(),
                ["Destination overview", "Visa info", "Search flights"])

        c = classify(message)
        session.last_intent = c.intent
        session.history.append({"role": "user", "text": message})

        if c.entities.get("flight_id"):
            session.last_flight_id = c.entities["flight_id"]
        if c.entities.get("hotel_id"):
            session.last_hotel_id = c.entities["hotel_id"]

        handler_map = {
            "greeting":         lambda: _handle_greeting(session),
            "goodbye":          lambda: _handle_goodbye(session),
            "thanks":           lambda: _handle_thanks(session),
            "search_flights":   lambda: _handle_search_flights(c, session),
            "flight_detail":    lambda: _handle_flight_detail(c, session),
            "search_hotels":    lambda: _handle_search_hotels(c, session),
            "hotel_detail":     lambda: _handle_hotel_detail(c, session),
            "view_packages":    lambda: _handle_view_packages(c, session),
            "destinations":     lambda: _handle_destinations(c, session),
            "build_itinerary":  lambda: _handle_build_itinerary(c, session),
            "view_bookings":    lambda: _handle_view_bookings(c, session),
            "booking_detail":   lambda: _handle_booking_detail(c, session),
            "checkin":          lambda: _handle_checkin(c, session),
            "weather":          lambda: _handle_weather(c, session),
            "visa_info":        lambda: _handle_visa_info(c, session),
            "cancel_modify":    lambda: _handle_cancel_modify(c, session),
            "loyalty_miles":    lambda: _handle_loyalty(c, session),
            "contact_support":  lambda: _handle_contact_support(c, session),
        }
        handler = handler_map.get(c.intent, lambda: _handle_unknown(c, session))
        blocks, suggestions = handler()

        return {
            "session_id":  session.session_id,
            "intent":      c.intent,
            "confidence":  c.confidence,
            "blocks":      blocks,
            "suggestions": suggestions,
            "safety_flag": None,
        }

    def _safety_response(self, session: Session, flag: str, block: dict, suggestions: list[str]):
        return {
            "session_id":  session.session_id,
            "intent":      f"{flag}_block",
            "confidence":  1.0,
            "blocks":      [block],
            "suggestions": suggestions,
            "safety_flag": flag,
        }


engine = ChatbotEngine()
