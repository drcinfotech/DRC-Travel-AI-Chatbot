"""
Intent classifier for the Travel & Hospitality chatbot.
Safety check (see safety.py) runs BEFORE this classifier.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class IntentSpec:
    name: str
    patterns: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)


INTENTS: list[IntentSpec] = [
    IntentSpec(
        "greeting",
        patterns=[r"^\s*(hi|hello|hey|hola|namaste|good (morning|afternoon|evening))\b"],
        keywords=["hi", "hello", "hey", "hola", "namaste"],
    ),
    IntentSpec(
        "goodbye",
        patterns=[r"\b(bye|goodbye|see ya|see you|cya|take care)\b"],
        keywords=["bye", "goodbye"],
    ),
    IntentSpec(
        "thanks",
        patterns=[r"^\s*(thanks|thank you|thx|ty|appreciate it)\b"],
        keywords=["thanks", "thank"],
    ),
    IntentSpec(
        "search_flights",
        patterns=[
            r"\b(find|search|show|book|need|looking for)\b.{0,30}\b(flights?|tickets?|airfare)\b",
            r"\bflights?\s+(from|to|between)\s+\w+",
            r"\b(fly|flying)\s+(to|from)\s+\w+",
            r"\bone[\s-]?way\b",
            r"\bround[\s-]?trip\b",
        ],
        keywords=["flight", "flights", "airfare", "fly to"],
    ),
    IntentSpec(
        "flight_detail",
        patterns=[
            r"\b(show|view|details? (of|on|for|about))\s+(this\s+)?flight\b",
            r"\bfl-?\d{3,5}\b",
            r"\bmore (info|details|about)\s+(this|that)\s+flight\b",
        ],
        keywords=["flight details", "fl-"],
    ),
    IntentSpec(
        "search_hotels",
        patterns=[
            r"\b(find|search|show|need|looking for)\b.{0,30}\b(hotels?|stays?|accommodation|resort|villa)\b",
            r"\bhotels?\s+(in|at|near)\s+\w+",
            r"\b(stay|accommodation)\s+(in|at|near)\s+\w+",
            r"\b(place|places)\s+to\s+stay\s+(in|at|near)",
        ],
        keywords=["hotel", "hotels", "stay", "accommodation", "resort"],
    ),
    IntentSpec(
        "hotel_detail",
        patterns=[
            r"\b(show|view|details? (of|on|for|about))\s+(this\s+)?(hotel|resort)\b",
            r"\bht-?\d{3,5}\b",
            r"\bmore (info|details|about)\s+(this|that)\s+(hotel|resort)\b",
        ],
        keywords=["hotel details", "ht-"],
    ),
    IntentSpec(
        "view_packages",
        patterns=[
            r"\b(holiday|travel|tour|trip)\s+packages?\b",
            r"\b(package|all[\s-]?inclusive)\s+(tour|deal|holiday|trip)",
            r"\b(show|list|find)\s+(me\s+)?packages?\b",
            r"\bcurated\s+(trips?|tours?|holidays?)\b",
        ],
        keywords=["packages", "tour package", "holiday package", "trip package"],
    ),
    IntentSpec(
        "destinations",
        patterns=[
            r"\b(tell me about|info on|describe|guide to)\s+(\w+\s+){0,3}(as\s+a\s+destination|destination)\b",
            r"\b(where\s+to\s+go|where\s+should\s+i\s+go|best\s+places)\b",
            r"\b(destination|destinations)\s+(guide|info|overview)\b",
            r"\babout\s+(goa|manali|jaisalmer|dubai|jaipur)\b",
        ],
        keywords=["destination", "destinations", "where to go"],
    ),
    IntentSpec(
        "build_itinerary",
        patterns=[
            r"\b(build|create|make|plan|suggest|give me)\s+(an?\s+)?(itinerary|day-?by-?day|trip\s+plan)",
            r"\b(\d+)\s*[\s-]?day\s+(itinerary|trip|plan|tour|trip\s+plan)\s+(for|to|in)?\s+\w*",
            r"\bday\s+by\s+day\s+(plan|itinerary)\b",
            r"\b(what\s+to\s+do\s+in)\s+\w+\s+(for\s+\d+\s+days?)?\b",
        ],
        keywords=["itinerary", "trip plan", "day by day", "what to do"],
    ),
    IntentSpec(
        "view_bookings",
        patterns=[
            r"\b(my|current|upcoming|active)\s+(bookings?|trips?|reservations?)\b",
            r"\b(show|view|list)\s+(me\s+)?(my\s+)?(bookings?|trips?|reservations?)",
            r"\bwhat'?s\s+on\s+my\s+(trip|travel|booking)\s+(list|schedule)",
        ],
        keywords=["my bookings", "my trips", "my reservations"],
    ),
    IntentSpec(
        "booking_detail",
        patterns=[
            r"\b(show|view|details? (of|on|for))\s+(booking\s+)?bk-?\d{3,6}\b",
            r"\bbk-?\d{3,6}\b",
        ],
        keywords=["booking details", "bk-"],
    ),
    IntentSpec(
        "checkin",
        patterns=[
            r"\b(web\s+)?check[\s-]?in\b",
            r"\b(can\s+i|how\s+to)\s+check[\s-]?in\b",
            r"\bget\s+(my\s+)?boarding\s+pass\b",
        ],
        keywords=["check-in", "check in", "boarding pass"],
    ),
    IntentSpec(
        "weather",
        patterns=[
            r"\bweather\s+(in|at|for)\s+\w+",
            r"\bhow'?s\s+(the\s+)?weather\s+(in|at|going to be)",
            r"\b(forecast|temperature)\s+(in|at|for)\s+\w+",
            r"\b(rainy|snowy|hot|cold|raining|snowing)\s+(in|at)\s+\w+",
        ],
        keywords=["weather", "forecast", "temperature"],
    ),
    IntentSpec(
        "visa_info",
        patterns=[
            r"\bvisa\s+(for|to|requirements?|process|info)\s+\w+",
            r"\bdo\s+i\s+need\s+(a\s+)?visa\s+(for|to)\s+\w+",
            r"\bwhat\s+visa\s+(do\s+i\s+need|is\s+required)\s+(for|to)\b",
            r"\bvisa\s+(documents?|paperwork|checklist|requirements?)\b",
        ],
        keywords=["visa", "visa requirements", "visa documents"],
    ),
    IntentSpec(
        "cancel_modify",
        patterns=[
            r"\b(cancel|modify|change|reschedule)\s+(my\s+)?(booking|flight|hotel|trip|reservation)",
            r"\b(refund|cancellation)\s+(policy|terms?|process)",
            r"\bget\s+a\s+refund\b",
            r"\bchange\s+(my\s+)?(travel|trip)\s+dates?\b",
        ],
        keywords=["cancel", "modify booking", "reschedule", "refund"],
    ),
    IntentSpec(
        "loyalty_miles",
        patterns=[
            r"\b(loyalty|frequent\s+flyer|miles|points|rewards?)\s+(program|account|balance)\b",
            r"\b(my\s+)?(skyline|northbound|coastline)\s+(miles|points|account)\b",
            r"\bhow\s+(many\s+)?(miles|points)\s+do\s+i\s+have\b",
            r"\bredeem\s+(my\s+)?(miles|points)\b",
        ],
        keywords=["miles", "loyalty", "frequent flyer", "rewards points"],
    ),
    IntentSpec(
        "contact_support",
        patterns=[
            r"\b(contact|talk to|speak to|reach)\s+(support|customer\s+(service|care)|help)",
            r"\b(human|real person|agent|representative)\b",
            r"\b(complaint|issue|problem)\s+(with|about|on)\s+(my\s+)?(booking|trip|flight|hotel)",
        ],
        keywords=["support", "customer service", "complaint"],
    ),
]


# ─── Entity extraction ─────────────────────────────────────
CITY_KEYWORDS = {
    "Mumbai":    ["mumbai", "bombay", "bom"],
    "Delhi":     ["delhi", "new delhi", "del"],
    "Goa":       ["goa", "goi"],
    "Manali":    ["manali"],
    "Jaisalmer": ["jaisalmer"],
    "Jaipur":    ["jaipur"],
    "Dubai":     ["dubai", "dxb"],
}


def extract_cities(text: str) -> dict:
    """Extract origin/destination cities from a flight query."""
    t = text.lower()
    found_with_prep = {"from": None, "to": None}
    found_plain = []

    # Try preposition-anchored extraction first
    for city, kws in CITY_KEYWORDS.items():
        for kw in kws:
            if re.search(rf"\bfrom\s+{re.escape(kw)}\b", t):
                found_with_prep["from"] = city
            if re.search(rf"\bto\s+{re.escape(kw)}\b", t):
                found_with_prep["to"] = city
            if re.search(rf"\b{re.escape(kw)}\b", t) and city not in found_plain:
                found_plain.append(city)

    return {**found_with_prep, "all": found_plain}


def extract_flight_id(text: str) -> Optional[str]:
    m = re.search(r"\bfl-?(\d{4,5})\b", text.lower())
    if m:
        return f"FL-{m.group(1)}"
    return None


def extract_hotel_id(text: str) -> Optional[str]:
    m = re.search(r"\bht-?(\d{4,5})\b", text.lower())
    if m:
        return f"HT-{m.group(1)}"
    return None


def extract_booking_id(text: str) -> Optional[str]:
    m = re.search(r"\bbk-?(\d{4,6})\b", text.lower())
    if m:
        return f"BK-{m.group(1)}"
    return None


def extract_nights(text: str) -> Optional[int]:
    """Extract '3-night', '5 night', '4 nights' etc."""
    m = re.search(r"\b(\d+)\s*[\s-]?nights?\b", text.lower())
    if m:
        return int(m.group(1))
    return None


def extract_days(text: str) -> Optional[int]:
    """Extract '3 day', '5 days' — for itinerary length."""
    m = re.search(r"\b(\d+)\s*[\s-]?days?\b", text.lower())
    if m:
        return int(m.group(1))
    return None


def extract_pax(text: str) -> Optional[int]:
    """Extract pax/guests/travelers count."""
    m = re.search(r"\b(\d+)\s+(pax|adults?|guests?|travel[le]?rs?|people|persons?)\b", text.lower())
    if m:
        return int(m.group(1))
    return None


# ─── Classifier ────────────────────────────────────────────
@dataclass
class Classification:
    intent: str
    confidence: float
    entities: dict


def classify(text: str) -> Classification:
    text_lc = text.lower().strip()

    scores: dict[str, float] = {}
    for spec in INTENTS:
        score = 0.0
        for p in spec.patterns:
            if re.search(p, text_lc, re.IGNORECASE):
                score += 2.0
        for kw in spec.keywords:
            if re.search(rf"\b{re.escape(kw)}\b", text_lc):
                score += 0.6
        if score > 0:
            scores[spec.name] = score

    # Disambiguation boosts
    if extract_booking_id(text):
        scores["booking_detail"] = scores.get("booking_detail", 0) + 1.5
    if extract_flight_id(text):
        scores["flight_detail"] = scores.get("flight_detail", 0) + 1.5
    if extract_hotel_id(text):
        scores["hotel_detail"] = scores.get("hotel_detail", 0) + 1.5

    if not scores:
        intent, conf = "unknown", 0.0
    else:
        intent = max(scores, key=scores.get)
        top = scores[intent]
        rest = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0.1
        conf = min(1.0, top / (top + rest))

    entities = {
        "cities":      extract_cities(text),
        "flight_id":   extract_flight_id(text),
        "hotel_id":    extract_hotel_id(text),
        "booking_id":  extract_booking_id(text),
        "nights":      extract_nights(text),
        "days":        extract_days(text),
        "pax":         extract_pax(text),
    }
    return Classification(intent=intent, confidence=round(conf, 2), entities=entities)
