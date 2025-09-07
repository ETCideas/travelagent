# ✈️ Travel Itinerary Orchestrator (Agent-based)

A ready-to-run Streamlit web app you can deploy in **GitHub Codespaces**. It uses simple, modular **agents** to:
- capture your preferences
- propose a day-by-day itinerary
- generate one-click links for flights, hotels, and experiences
- add extra suggestions from light-weight heuristics (no paid APIs required)

> You can later plug in LLMs or travel APIs (Amadeus, Skyscanner, Booking.com, GetYourGuide, etc.).

---

## 🚀 Quick Start (on GitHub Mobile + Codespaces)

1. Upload the ZIP to a new GitHub repo (tap **+** → **Upload**).
2. In the repo, open **Code** → **Codespaces** → **Create codespace on main**.
3. Wait for dependencies to install (done automatically via `.devcontainer`).
4. In the terminal, run:
   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```
5. Click the forwarded **8501** port to open your web app.

---

## 🧩 Architecture

- `agents/orchestrator.py` — runs agents in order and merges outputs into a shared context.
- `agents/preference_agent.py` — validates and summarizes the user’s preferences.
- `agents/flight_agent.py` — builds deep links to Google Flights & Skyscanner.
- `agents/hotel_agent.py` — builds deep links to Booking.com & Hotels.com.
- `agents/experience_agent.py` — links to GetYourGuide, Viator, and a Google search.
- `agents/suggestion_agent.py` — proposes a basic itinerary and food ideas, plus quick-search links.
- `utils/` — link builders, itinerary heuristics, and pydantic validators.
- `data/` — simple cuisine suggestions (expand freely).

No external API keys required. If you want to use OpenAI or travel APIs, add a new agent and inject keys with environment variables.

---

## 🛠️ Customize

- Add/remove cities and tune the itinerary heuristic in `utils/itinerary.py`.
- Add cuisine packs in `data/cuisine_suggestions.json`.
- Add new providers in `utils/link_builders.py` (Kayak, Expedia, Airbnb, Klook, etc.).
- Add an `llm_agent.py` to refine the plan with your preferred model.

---

## 📦 Requirements

- Python 3.11+ (Codespaces image provides this)
- `pip install -r requirements.txt` (handled by devcontainer)

---

## ✅ Why this design?

- **Modular agents** keep logic tidy and replaceable.
- **No scraping**: we generate reputable booking/search links with prefilled parameters.
- **Mobile-friendly**: upload once, run in Codespaces, share a URL.
- **Privacy-first**: all inputs stay in your session (no server DB by default).

---

## 🧪 Local Run (optional)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 📄 License

MIT — do anything, just keep the notice.
