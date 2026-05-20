"""
Safety layer for the Travel & Hospitality chatbot.

This module handles:
  • Booking fraud — refuses to "confirm" bookings outside the real flow,
    refuses to fabricate PNRs / confirmation numbers, refuses to share
    another traveler's data (which would be a privacy + scam risk).
  • Travel-advisory honesty — declines to make sweeping safety/political
    judgments about destinations ("is X country safe?", "should I avoid Y?").
    Real travel chatbots that confidently answer these have caused real harm
    when their assessments are wrong or politically loaded. We redirect to
    official government advisories instead.
  • Visa / immigration disclaimer — won't act as an immigration consultant.
  • Payment privacy — same as other bots; chat is never an appropriate
    channel for card numbers, OTPs, or PINs.
  • Social engineering / prompt injection — same baseline.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Literal


@dataclass
class SafetyResult:
    flag: Optional[Literal[
        "booking_fraud",
        "travel_advisory",
        "visa_consult",
        "payment_privacy",
        "social_engineering"
    ]] = None
    reason: str = ""


# ─── Booking fraud / impersonation ────────────────────────
# Refuse to "confirm" a booking outside the actual flow, to fabricate PNRs,
# or to share another person's data.
BOOKING_FRAUD_PATTERNS = [
    # "Confirm" / "guarantee" a booking we don't actually have
    r"\b(confirm|guarantee|finalize|finalise)\s+(my\s+)?(booking|reservation|seat|room)\b.{0,30}\b(without|outside|skip(?:ping)?)\s+(payment|verification|booking\s+flow)",
    # Asking us to invent a PNR / confirmation number
    r"\b(give|create|generate|make up|fabricate|invent)\s+(me\s+)?(a\s+)?(fake|valid|real)?\s*(pnr|confirmation\s+(code|number)|booking\s+(id|number|reference))\b",
    r"\b(any|random)\s+(pnr|confirmation\s+code|booking\s+reference)\s+(will\s+do|that\s+works|please)\b",
    # Trying to look up someone else's booking
    r"\b(look\s+up|find|show)\s+(someone(?:\s+else)?'?s|other\s+person'?s|another'?s)\s+(booking|pnr|reservation|trip)",
    r"\b(my\s+friend'?s|my\s+wife'?s|my\s+husband'?s|my\s+colleague'?s)\s+(booking|pnr)\s+(without|skip|bypass)\b",
    # Pretending to be the airline / hotel
    r"\bpretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(airline|hotel|booking\s+agent|travel\s+agent)\s+(with\s+full\s+access|backend)",
]


# ─── Travel-advisory sweeping judgments ───────────────────
# Refuse to confidently judge entire countries as safe/unsafe.
# This is a political minefield AND a real risk vector: if a chatbot tells
# someone "yes, country X is safe to visit right now" and there's an active
# advisory, the chatbot is contributing to real harm.
TRAVEL_ADVISORY_PATTERNS = [
    r"\bis\s+(it\s+)?safe\s+to\s+(travel\s+to|visit|go\s+to|fly\s+to)\s+\w+",
    r"\b(is|are)\s+([A-Z][a-z]+|\w+)\s+(safe|dangerous|unsafe|risky)\s+(to\s+visit|right\s+now|for\s+(tourists|indians|americans|foreigners))",
    r"\bshould\s+i\s+(avoid|skip|cancel)\s+(travel(?:ing)?\s+to|going\s+to|my\s+trip\s+to)\s+\w+",
    r"\b(tell|warn)\s+me\s+(about|if)\s+(the\s+)?(political\s+situation|war|conflict|civil\s+unrest|protests?)\s+in\s+\w+",
    r"\bwhich\s+countries?\s+are\s+(safe|dangerous|unsafe|too\s+risky)\b",
]


# ─── Visa / immigration consultation ──────────────────────
# We provide GENERAL info (we have a VisaBlock that names doc types) but
# refuse to act as a personalized immigration consultant on detailed
# eligibility, denials, appeals, or asylum.
VISA_CONSULT_PATTERNS = [
    # Asylum / refugee status — never our domain
    r"\bhow\s+(do\s+i|can\s+i)\s+(apply\s+for|get|claim)\s+(asylum|refugee\s+status)\b",
    r"\b(asylum|refugee)\s+(application|process|claim)\b",
    # Visa denials / appeals — needs a real lawyer
    r"\bmy\s+visa\s+(was\s+)?(denied|rejected|refused)\b",
    r"\bappeal\s+(a\s+|my\s+)?visa\s+(denial|rejection|refusal)",
    # Detailed eligibility for complex categories
    r"\bcan\s+i\s+(get|apply\s+for)\s+(a\s+)?(green\s+card|permanent\s+resid|h-?1b|o-?1|eb-?[1-5]|investor\s+visa|golden\s+visa)\b",
    # Overstay / illegal status
    r"\bi\s+(overstayed|have\s+overstayed)\s+my\s+visa\b",
    r"\bwhat\s+if\s+i\s+stay\s+(past|beyond|after)\s+my\s+visa\b",
]


# ─── Payment privacy ──────────────────────────────────────
PAYMENT_PRIVACY_PATTERNS = [
    r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
    r"\bcvv\s+(is|number|code|value)\s+(\w+\s+)?\d{3,4}\b",
    r"\bcvv\s+code\s+is\s+\d{3,4}\b",
    r"\b(my|the|save|store)\s+(card|credit\s+card|debit\s+card)\s+(number|details?|info)\s+is\b",
    r"\b(remember|memorize|store|save)\s+my\s+(card|cvv|pin|password|otp)",
    r"\bbypass\s+(payment|otp|cvv|verification|3d\s*secure)",
    r"\bskip\s+(payment|otp|verification|2fa|3d\s*secure)",
]


# ─── Social engineering ───────────────────────────────────
SOCIAL_ENGINEERING_PATTERNS = [
    r"\b(ignore|disregard|forget)\s+(\w+\s+){0,4}(instructions|rules|guidelines|system\s+prompt|safety)",
    r"\byou\s+are\s+now\s+(in\s+|an?\s+)?(admin|administrator|dev|developer|debug|root|owner|airline\s+staff)\s+(mode|user)?",
    r"\bpretend\s+(you\s+are|to\s+be)\s+(an?\s+)?(admin|root|developer|airline\s+staff|hotel\s+manager\s+with\s+full\s+access)",
    r"\b(give|provide|reveal|show|tell)\s+(me\s+)?(your\s+)?(system\s+prompt|instructions|api\s+key|source\s+code)",
    r"\benable\s+(developer|admin|debug|root)\s+mode\b",
    r"\bjailbreak\b",
    r"\bDAN\s+mode\b",
    r"\bact\s+as\s+(if\s+)?(you\s+have\s+)?no\s+(rules|restrictions|guidelines|safety)",
    r"\b(give\s+me\s+)?(free|complimentary)\s+(flight|hotel|booking|upgrade)\s+(for\s+me\s+)?(please\s+)?(now)?\b",
]


def check_safety(text: str) -> SafetyResult:
    t = text.lower()

    for pat in SOCIAL_ENGINEERING_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="social_engineering", reason=pat)
    for pat in PAYMENT_PRIVACY_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="payment_privacy", reason=pat)
    for pat in BOOKING_FRAUD_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="booking_fraud", reason=pat)
    for pat in VISA_CONSULT_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="visa_consult", reason=pat)
    for pat in TRAVEL_ADVISORY_PATTERNS:
        if re.search(pat, t):
            return SafetyResult(flag="travel_advisory", reason=pat)

    return SafetyResult(flag=None)


# ─── Block builders ───────────────────────────────────────
def build_booking_fraud_block() -> dict:
    return {
        "type": "travel_alert",
        "headline": "I can't fabricate or manipulate bookings.",
        "message": (
            "I won't create fake PNRs, confirmation numbers, or 'confirm' a booking outside the actual "
            "booking flow with payment. I also can't look up another person's booking on their behalf "
            "without proper authorization — that's a privacy and fraud-prevention boundary."
        ),
        "indicators": [
            "Real PNRs are issued by the airline's GDS only after payment clears",
            "Faked confirmation codes are a common scam — never trust one shared in chat",
            "Looking up someone else's booking requires their consent and identity verification",
        ],
        "offer": (
            "What I CAN do: search flights/hotels with you, walk you through booking steps, "
            "and show YOUR confirmed bookings in this demo. Want to do any of those?"
        ),
    }


def build_travel_advisory_block() -> dict:
    return {
        "type": "travel_alert",
        "headline": "I can't make sweeping safety calls on countries.",
        "message": (
            "Whether a destination is 'safe' depends on your nationality, the specific region within the "
            "country, current events, your activities, and your travel insurance — it changes daily. "
            "I'm not the right source for that judgment, and getting it wrong puts real travelers at risk. "
            "Please rely on official government travel advisories instead."
        ),
        "indicators": [
            "India: Ministry of External Affairs — mea.gov.in (Travel Advisories)",
            "US: travel.state.gov · UK: gov.uk/foreign-travel-advice",
            "EU: re-open.europa.eu · Canada: travel.gc.ca",
            "Advisories list specific regions, not just whole countries",
        ],
        "offer": (
            "What I CAN do: tell you about logistics for a destination (best season, currency, language, "
            "general visa category, ideal trip length), or help you book flights/hotels. Want either?"
        ),
    }


def build_visa_consult_block() -> dict:
    return {
        "type": "travel_alert",
        "headline": "Visa specifics need a real consultant.",
        "message": (
            "Visa eligibility, denial appeals, asylum applications, and immigration status questions are "
            "consequential enough that you should talk to a registered immigration lawyer or the official "
            "embassy of the destination country. I can share general categories but not personalized advice "
            "on these — getting it wrong has real legal and life consequences."
        ),
        "indicators": [
            "Visa rules change frequently — never trust outdated chatbot info",
            "Denial appeals and asylum applications have strict deadlines",
            "Immigration lawyers (bar-registered) are the right resource",
            "Embassy / consulate websites have the definitive current rules",
        ],
        "offer": (
            "What I CAN do: tell you the typical visa category for a destination (tourist, business), "
            "the documents usually required, and point you at the embassy website. Want that overview?"
        ),
    }


def build_payment_privacy_block() -> dict:
    return {
        "type": "travel_alert",
        "headline": "Don't share card details in chat.",
        "message": (
            "I can't accept or store full card numbers, CVV, OTP, or PIN through chat — that's a security "
            "risk regardless of who's asking. Real bookings go through encrypted payment gateways with "
            "PCI-DSS compliance, not free-text chat fields."
        ),
        "indicators": [
            "Card details typed in chat may be logged in plaintext",
            "Legitimate payment flows always use a dedicated, encrypted UI",
            "OTPs and PINs should NEVER be shared with anyone — including chatbots",
            "Travel-payment scams often start with 'just confirm your card details here'",
        ],
        "offer": "When you're ready to pay, the booking flow handles cards / UPI / wallets through a proper gateway. Ask me to take you to checkout and I will.",
    }


def build_social_engineering_block() -> dict:
    return {
        "type": "travel_alert",
        "headline": "I can't do that.",
        "message": (
            "I won't bypass my safety rules, switch into 'admin' mode, give you free flights/hotels/upgrades, "
            "or reveal internal instructions. If you have a real travel question, I'm happy to help with that."
        ),
        "indicators": [
            "I work the same way for everyone — there's no privileged mode",
            "Real airline / hotel agents can do things I can't (comps, upgrades, refunds)",
            "Use 'Contact support' for anything beyond search and booking tools",
        ],
        "offer": "Try asking about flights, hotels, packages, destinations, or your bookings.",
    }
