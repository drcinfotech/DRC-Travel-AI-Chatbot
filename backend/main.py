"""FastAPI entry point for the Travel & Hospitality AI Chatbot."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.catalog import catalog
from app.chatbot import engine
from app.models import ChatRequest, ChatResponse
from app.sessions import store

app = FastAPI(
    title="Travel AI Chatbot — Trip Assistant",
    description=(
        "A demo conversational AI for the travel and hospitality industry. "
        "Includes intent classification, booking-fraud guardrails, travel-advisory "
        "honesty, visa-consult disclaimers, payment privacy, and rich response "
        "blocks for flights, hotels, packages, destinations, itineraries, bookings, "
        "weather, and visa info. NOT a real OTA or travel agency."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status":       "ok",
        "flights":      len(catalog.flights()),
        "hotels":       len(catalog.hotels()),
        "packages":     len(catalog.packages()),
        "destinations": len(catalog.destinations()),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session = store.get_or_create(req.session_id)
    return engine.respond(req.message, session)


@app.get("/flights")
def list_flights():
    return catalog.flights()


@app.get("/flights/{fid}")
def get_flight(fid: str):
    f = catalog.flight(fid)
    if not f:
        return {"error": "not_found", "id": fid}
    return f


@app.get("/hotels")
def list_hotels():
    return catalog.hotels()


@app.get("/hotels/{hid}")
def get_hotel(hid: str):
    h = catalog.hotel(hid)
    if not h:
        return {"error": "not_found", "id": hid}
    return h


@app.get("/packages")
def list_packages():
    return catalog.packages()


@app.get("/bookings")
def list_bookings():
    return catalog.bookings()


@app.get("/destinations")
def list_destinations():
    return catalog.destinations()


@app.get("/")
def root():
    return {
        "name":       "Travel AI Chatbot — Trip Assistant",
        "version":    app.version,
        "docs":       "/docs",
        "disclaimer": "Demo only. Not a real OTA or travel agency.",
    }
