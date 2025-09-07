import streamlit as st
from datetime import date
from typing import Dict, Any, List
from agents.orchestrator import Orchestrator
from agents.preference_agent import PreferenceAgent
from agents.flight_agent import FlightAgent
from agents.hotel_agent import HotelAgent
from agents.experience_agent import ExperienceAgent
from agents.suggestion_agent import SuggestionAgent

st.set_page_config(page_title="Travel Itinerary Orchestrator", page_icon="✈️", layout="wide")

st.title("✈️ Travel Itinerary Orchestrator")
st.caption("Agent-based planner that gathers your preferences, proposes an itinerary, and gives one-click links for flights, stays, and experiences.")

with st.sidebar:
    st.header("Your Trip Details")
    with st.form("pref_form", clear_on_submit=False):
        name = st.text_input("Your name", value="Traveler")
        email = st.text_input("Email (optional)", value="")
        origin = st.text_input("Departure airport/city (IATA like DEL, BOM is great)", value="DEL")
        dests = st.text_input("Destination cities (comma-separated)", value="Paris, Rome")

        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("Start date", value=date.today())
        with col2:
            end = st.date_input("End date", value=date.today())

        col3, col4, col5 = st.columns(3)
        with col3:
            adults = st.number_input("Adults", min_value=0, value=2, step=1)
        with col4:
            children = st.number_input("Children", min_value=0, value=0, step=1)
        with col5:
            rooms = st.number_input("Rooms", min_value=1, value=1, step=1)

        likes = st.text_input("What do you love? (comma-separated)", value="architecture, coffee, photography")
        dislikes = st.text_input("What to avoid? (comma-separated)", value="long queues")
        cuisine_focus = st.text_input("Cuisine focus (e.g., Italy, Japan, default)", value="default")

        submitted = st.form_submit_button("Build Itinerary 🚀")

def _prep_context() -> Dict[str, Any]:
    destinations = [d.strip() for d in dests.split(",") if d.strip()]
    prefs = {
        "name": name,
        "email": email or None,
        "origin": origin,
        "destinations": destinations,
        "start_date": str(start),
        "end_date": str(end),
        "likes": [s.strip() for s in (likes or "").split(",") if s.strip()],
        "dislikes": [s.strip() for s in (dislikes or "").split(",") if s.strip()],
        "cuisine_focus": cuisine_focus or None,
        "traveler": {"adults": int(adults), "children": int(children), "rooms": int(rooms)}
    }
    return {"preferences": prefs}

if submitted:
    context = _prep_context()
    agents = [PreferenceAgent(), FlightAgent(), HotelAgent(), ExperienceAgent(), SuggestionAgent()]
    orch = Orchestrator(agents)
    results = orch.run(context)

    # Display preference summary
    pref = [r for r in results if r.name == "preference_agent"][0].payload.get("preference_summary", {})
    st.subheader("Your Preference Summary")
    st.json(pref, expanded=False)

    # Flights
    fl = [r for r in results if r.name == "flight_agent"][0].payload.get("flights", {})
    st.subheader("✈️ Flights")
    cols = st.columns(2)
    with cols[0]:
        st.markdown("**To first city**")
        for label, url in fl.get("to_first_city", {}).get("links", {}).items():
            st.link_button(label, url)
    with cols[1]:
        st.markdown("**Return**")
        for label, url in fl.get("return", {}).get("links", {}).items():
            st.link_button(label, url)

    # Hotels
    st.subheader("🏨 Hotels")
    hotels = [r for r in results if r.name == "hotel_agent"][0].payload.get("hotels", {})
    for city, links in hotels.items():
        with st.expander(f"{city}"):
            for label, url in links.items():
                st.link_button(label, url)

    # Experiences
    st.subheader("🎟️ Experiences & Things To Do")
    exps = [r for r in results if r.name == "experience_agent"][0].payload.get("experiences", {})
    for city, links in exps.items():
        with st.expander(f"{city}"):
            for label, url in links.items():
                st.link_button(label, url)

    # Itinerary & Food
    st.subheader("🗺️ Draft Itinerary")
    it_payload = [r for r in results if r.name == "suggestion_agent"][0].payload
    plan = it_payload.get("itinerary", [])
    food = it_payload.get("food_suggestions", [])
    for day in plan:
        with st.expander(f"{day['date']} — {day['city']}"):
            st.markdown(f"**Morning:** {day['morning']}\n\n**Afternoon:** {day['afternoon']}\n\n**Evening:** {day['evening']}")
            st.caption("Quick searches:")
            for label, url in day.get("suggested_searches", {}).items():
                st.link_button(label, url)

    st.subheader("🍽️ Food Suggestions")
    for idea in food:
        st.markdown(f"- {idea}")

    st.success("Done! Use the buttons above to book and refine.")
else:
    st.info("Fill the form on the left and click **Build Itinerary 🚀** to get started.")
