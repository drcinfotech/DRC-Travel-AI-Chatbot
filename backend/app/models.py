"""
Pydantic models for the Travel & Hospitality chatbot.
"""
from __future__ import annotations

from typing import Optional, Literal
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)
    session_id: Optional[str] = None


class TextBlock(BaseModel):
    type: Literal["text"] = "text"
    content: str


class DisclaimerBlock(BaseModel):
    type: Literal["disclaimer"] = "disclaimer"
    content: str


class TravelAlertBlock(BaseModel):
    """Shown when a safety guard fires."""
    type: Literal["travel_alert"] = "travel_alert"
    headline: str
    message: str
    indicators: list[str]
    offer: str


class FlightListBlock(BaseModel):
    type: Literal["flight_list"] = "flight_list"
    title: Optional[str] = None
    route: Optional[dict] = None     # {from, to, date}
    items: list[dict]
    total: int


class FlightDetailBlock(BaseModel):
    type: Literal["flight_detail"] = "flight_detail"
    flight: dict


class HotelListBlock(BaseModel):
    type: Literal["hotel_list"] = "hotel_list"
    title: Optional[str] = None
    items: list[dict]
    total: int


class HotelDetailBlock(BaseModel):
    type: Literal["hotel_detail"] = "hotel_detail"
    hotel: dict


class PackageBlock(BaseModel):
    type: Literal["package"] = "package"
    title: Optional[str] = None
    items: list[dict]


class DestinationBlock(BaseModel):
    type: Literal["destination"] = "destination"
    items: list[dict]


class ItineraryBlock(BaseModel):
    type: Literal["itinerary"] = "itinerary"
    destination: str
    nights: int
    days: int
    day_plan: list[dict]    # [{day, title, activities}]
    note: Optional[str] = None


class BookingsBlock(BaseModel):
    type: Literal["bookings"] = "bookings"
    items: list[dict]


class BookingConfirmationBlock(BaseModel):
    type: Literal["booking_confirmation"] = "booking_confirmation"
    booking: dict


class CheckInBlock(BaseModel):
    type: Literal["check_in"] = "check_in"
    booking_id: str
    flight: dict
    passenger: dict
    seat: Optional[str] = None
    boarding_pass_ready: bool


class WeatherBlock(BaseModel):
    type: Literal["weather"] = "weather"
    destination: str
    forecast: list[dict]   # [{date, high, low, conditions}]
    note: str


class VisaBlock(BaseModel):
    type: Literal["visa"] = "visa"
    destination: str
    country: str
    summary: str
    documents: list[dict]
    note: str


MessageBlock = (
    TextBlock | DisclaimerBlock | TravelAlertBlock
    | FlightListBlock | FlightDetailBlock | HotelListBlock | HotelDetailBlock
    | PackageBlock | DestinationBlock | ItineraryBlock
    | BookingsBlock | BookingConfirmationBlock | CheckInBlock
    | WeatherBlock | VisaBlock
)


class ChatResponse(BaseModel):
    session_id: str
    intent: str
    confidence: float
    blocks: list[MessageBlock]
    suggestions: list[str] = []
    safety_flag: Optional[str] = None
