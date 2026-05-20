"""Data catalog — loads catalog from JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


DATA_DIR = Path(__file__).parent.parent / "data"


class Catalog:
    def __init__(self):
        with open(DATA_DIR / "catalog.json", "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def flights(self) -> list[dict]:
        return list(self._data["flights"])

    def flight(self, fid: str) -> Optional[dict]:
        for f in self._data["flights"]:
            if f["id"] == fid:
                return f
        return None

    def hotels(self) -> list[dict]:
        return list(self._data["hotels"])

    def hotel(self, hid: str) -> Optional[dict]:
        for h in self._data["hotels"]:
            if h["id"] == hid:
                return h
        return None

    def packages(self) -> list[dict]:
        return list(self._data["packages"])

    def bookings(self) -> list[dict]:
        return list(self._data["bookings"])

    def booking(self, bid: str) -> Optional[dict]:
        for b in self._data["bookings"]:
            if b["id"] == bid:
                return b
        return None

    def destinations(self) -> list[dict]:
        return list(self._data["destinations"])

    def destination(self, name: str) -> Optional[dict]:
        n = name.lower()
        for d in self._data["destinations"]:
            if d["name"].lower() == n or d["id"].lower().endswith(n):
                return d
        return None


catalog = Catalog()
