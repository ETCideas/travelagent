from urllib.parse import quote, urlencode
from datetime import datetime

def _fmt_date(dt_str: str) -> str:
    """Return YYYY-MM-DD (for most travel sites)."""
    try:
        return datetime.fromisoformat(dt_str).strftime("%Y-%m-%d")
    except Exception:
        return dt_str

def google_flights_link(origin: str, dest: str, depart: str, return_: str | None, adults: int = 1, children: int = 0):
    depart = _fmt_date(depart)
    if return_:
        return_ = _fmt_date(return_)
    pax = f"{adults}a{children}c"
    if return_:
        path = f"/flights?hl=en#flt={origin}.{dest}.{depart}*{dest}.{origin}.{return_};c:{pax};so:1"
    else:
        path = f"/flights?hl=en#flt={origin}.{dest}.{depart};c:{pax};so:1"
    return f"https://www.google.com{path}"

def skyscanner_link(origin: str, dest: str, depart: str, return_: str | None, adults: int = 1, children: int = 0):
    depart = _fmt_date(depart)
    if return_:
        return_ = _fmt_date(return_)
    base = "https://www.skyscanner.net/transport/flights/"
    od = f"{origin}/{dest}/{depart}/"
    qp = urlencode({"adults": adults, "children": children})
    if return_:
        od = f"{origin}/{dest}/{depart}/{return_}/"
    return f"{base}{od}?{qp}"

def booking_dot_com_link(city: str, checkin: str, checkout: str, rooms: int, adults: int, children: int):
    base = "https://www.booking.com/searchresults.html"
    q = {
        "ss": city,
        "checkin": _fmt_date(checkin),
        "checkout": _fmt_date(checkout),
        "group_adults": adults,
        "group_children": children,
        "no_rooms": rooms
    }
    return f"{base}?{urlencode(q)}"

def hotels_dot_com_link(city: str, checkin: str, checkout: str, rooms: int, adults: int, children: int):
    base = "https://www.hotels.com/Hotel-Search"
    q = {
        "destination": city,
        "check-in": _fmt_date(checkin),
        "check-out": _fmt_date(checkout),
        "rooms": rooms,
        "adults": adults,
        "children": children
    }
    return f"{base}?{urlencode(q)}"

def getyourguide_link(city: str, query: str = "things to do"):
    base = "https://www.getyourguide.com/s/"
    return f"{base}{quote(city)}/?q={quote(query)}"

def viator_link(city: str, query: str = "tours and activities"):
    base = "https://www.viator.com/searchResults/all"
    q = {"text": f"{city} {query}"}
    return f"{base}?{urlencode(q)}"

def google_maps_search(query: str):
    return f"https://www.google.com/maps/search/{quote(query)}"

def generic_web_search(query: str):
    return f"https://www.google.com/search?q={quote(query)}"
