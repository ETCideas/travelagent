from typing import Dict, Any
from ..utils.link_builders import booking_dot_com_link, hotels_dot_com_link

class HotelAgent:
    name = "hotel_agent"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        p = context["preference_summary"]
        cities = p["destinations"]
        start = p["travel_window"]["start"]
        end = p["travel_window"]["end"]
        adults = p["adults"]
        children = p["children"]
        rooms = p["rooms"]
        hotel_links = {}
        for c in cities:
            hotel_links[c] = {
                "Booking.com": booking_dot_com_link(c, start, end, rooms, adults, children),
                "Hotels.com": hotels_dot_com_link(c, start, end, rooms, adults, children)
            }
        return {"hotels": hotel_links}
