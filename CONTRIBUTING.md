# Contributing to Trip Assistant

Thanks for your interest! This is a demo of conversational AI for the travel and hospitality domain, so contributions are welcome — but **travel-safety-critical code paths have extra rules**.

## Code of conduct

Be kind. Disagree on technical merits, not on people.

## Quick start for contributors

```bash
git clone https://github.com/drcinfotech/Travel-AI-Chatbot.git
cd Travel-AI-Chatbot

# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
pytest -v       # must be 61/61 green before you start

# Frontend
cd ../frontend
npm install
npm run dev
```

## What we accept

✅ **Good contributions:**

- New intents with corresponding tests
- New block renderers in `Blocks.jsx` with corresponding Pydantic models
- New curated itineraries for destinations (must be fictional / illustrative)
- More fictional airlines, hotels, packages, destinations (invented brands only)
- Documentation, README improvements, screenshots
- Accessibility improvements
- i18n / localization support
- Tighter test coverage

❌ **What we do NOT accept:**

- Real airline, hotel chain, or OTA brand names. The CI test `test_no_real_travel_brands_in_data` will fail your PR.
- Removing or weakening the booking-fraud refusal
- Adding "guarantees" about country-level safety — that's exactly what we refuse
- Removing the travel-advisory redirect to government sources
- Removing or weakening visa-consult disclaimers
- Removing payment-privacy guards
- Removing or relaxing prompt-injection blocks
- Real PNRs, real confirmation numbers, real travel-agent IATA codes
- Adding personal API keys, payment gateway credentials, or real card data
- Code that connects to real GDS / payment processors without explicit opt-in and clear documentation
- Replacing "Trip Assistant" with an unverified brand name

## Travel-safety rule changes (require extra review)

Any PR that modifies the following files **must** include test coverage and a written rationale in the PR description:

- `backend/app/safety.py` — booking-fraud, travel-advisory, visa-consult, payment privacy, social engineering
- `backend/app/chatbot.py` — the safety-first dispatch
- `backend/data/catalog.json` — particularly any travel-advisory or visa-related content
- Any change that touches how refusal blocks are surfaced in the UI

**The default position when in doubt:** decline to make confident claims about country-level safety, visa eligibility, or booking validity. Travel scams thrive on false confidence from chatbots. When unsure whether a query is "asking for help with logistics" (which we DO help with) vs "asking us to make a binding safety/legal judgment" (which we DON'T), bias toward the refusal pattern with a redirect to the appropriate authority.

## Adding a new destination

If you add a new destination to `catalog.json`, please:

- [ ] Use a real city name (these aren't brand-trademarked) but don't reference real airlines or hotels there
- [ ] Add a `visa_note` field that's accurate at a general level
- [ ] If it's an international destination, don't make claims about current safety — just describe what's there
- [ ] If you add a curated `ITINERARY_TEMPLATE` in chatbot.py, mark activities as "in season" / "if open" / "subject to weather" where appropriate

## Style

- Python: PEP 8, type hints on public functions, docstrings on modules
- JS/JSX: 2-space indent, prefer functional components, hooks for state
- Commits: imperative present tense ("Add X", "Fix Y")
- One logical change per PR

## Reporting a security issue

For anything that looks like a real security issue (not just a demo limitation), please email the maintainers privately rather than opening a public issue.
