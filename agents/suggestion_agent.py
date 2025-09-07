import json
from typing import Dict, Any, List
from pathlib import Path
from ..utils.itinerary import build_basic_itinerary
from ..utils.link_builders import generic_web_search, google_maps_search

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "cuisine_suggestions.json"

class SuggestionAgent:
    name = "suggestion_agent"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        p = context["preference_summary"]
        start = p["travel_window"]["start"]
        end = p["travel_window"]["end"]
        cities = p["destinations"]
        cuisine_focus = (p.get("cuisine_focus") or "default")
        with open(DATA_PATH, "r") as f:
            cuisine = json.load(f)
        food_ideas: List[str] = cuisine.get(cuisine_focus, cuisine.get("default", []))
        plan = build_basic_itinerary(cities, start, end)
        # Enrich each day with quick search links
        for day in plan:
            city = day["city"]
            day["suggested_searches"] = {
                "Google: day plan": generic_web_search(f"{city} one-day itinerary"),
                "Maps: food near you": google_maps_search(f"best food in {city}"),
                "Hidden gems": generic_web_search(f"hidden gems in {city}")
            }
        return {"itinerary": plan, "food_suggestions": food_ideas}
