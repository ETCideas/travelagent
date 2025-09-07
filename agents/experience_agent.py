from typing import Dict, Any
from ..utils.link_builders import getyourguide_link, viator_link, generic_web_search

class ExperienceAgent:
    name = "experience_agent"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        p = context["preference_summary"]
        links = {}
        for c in p["destinations"]:
            links[c] = {
                "GetYourGuide": getyourguide_link(c),
                "Viator": viator_link(c),
                "Top sights (Google)": generic_web_search(f"best things to do in {c}")
            }
        return {"experiences": links}
