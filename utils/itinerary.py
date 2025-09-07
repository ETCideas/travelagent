from datetime import datetime, timedelta
from typing import List, Dict

def daterange(start_date: datetime, end_date: datetime):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def build_basic_itinerary(cities: List[str], start_date: str, end_date: str) -> List[Dict]:
    """Simple heuristic itinerary: morning/afternoon/evening blocks per day."""
    sd = datetime.fromisoformat(start_date)
    ed = datetime.fromisoformat(end_date)
    days = list(daterange(sd, ed))
    if not days:
        return []
    # Distribute days roughly equally across cities
    per_city = max(1, len(days) // max(1, len(cities)))
    plan = []
    idx = 0
    for city in cities:
        for _ in range(per_city):
            if idx >= len(days): break
            day = days[idx]
            plan.append({
                "date": day.strftime("%Y-%m-%d"),
                "city": city,
                "morning": "Landmarks & viewpoints (start early to beat crowds)",
                "afternoon": "Museums / neighborhoods walk / markets",
                "evening": "Food crawl & sunset spot"
            })
            idx += 1
    # leftover days stay in last city
    while idx < len(days):
        day = days[idx]
        plan.append({
            "date": day.strftime("%Y-%m-%d"),
            "city": cities[-1],
            "morning": "Local experience (class/workshop)",
            "afternoon": "Parks / waterfront / short hike",
            "evening": "Dinner with a view / show"
        })
        idx += 1
    return plan
