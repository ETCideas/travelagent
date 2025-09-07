from typing import Dict, Any, List
from ..utils.link_builders import google_flights_link, skyscanner_link

class FlightAgent:
    name = "flight_agent"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        p = context["preference_summary"]
        origin = p["origin"]
        dests: List[str] = p["destinations"]
        start = p["travel_window"]["start"]
        end = p["travel_window"]["end"]
        adults = p["adults"]
        children = p["children"]
        # Simple: first destination is primary
        primary_dest = dests[0]
        out = {
            "flights": {
                "to_first_city": {
                    "origin": origin,
                    "destination": primary_dest,
                    "depart": start,
                    "links": {
                        "Google Flights": google_flights_link(origin, primary_dest, start, None, adults, children),
                        "Skyscanner": skyscanner_link(origin, primary_dest, start, None, adults, children)
                    }
                },
                "return": {
                    "origin": dests[-1],
                    "destination": origin,
                    "return": end,
                    "links": {
                        "Google Flights": google_flights_link(dests[-1], origin, end, None, adults, children),
                        "Skyscanner": skyscanner_link(dests[-1], origin, end, None, adults, children)
                    }
                }
            }
        }
        return out
