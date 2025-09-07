import json
from typing import Dict, Any
from ..utils.validators import PreferenceInput

class PreferenceAgent:
    name = "preference_agent"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Context should already carry user form data
        data = PreferenceInput(**context["preferences"])  # type: ignore
        # Persist summarized preferences
        summary = {
            "traveler_name": data.name,
            "origin": data.origin.upper(),
            "destinations": data.destinations,
            "travel_window": {"start": data.start_date, "end": data.end_date},
            "likes": data.likes,
            "dislikes": data.dislikes,
            "cuisine_focus": data.cuisine_focus or "default",
            "adults": data.traveler.adults,
            "children": data.traveler.children,
            "rooms": data.traveler.rooms,
        }
        return {"preference_summary": summary}
