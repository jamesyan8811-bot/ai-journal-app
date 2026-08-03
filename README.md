# James AI Journal Club App

A GitHub- and Streamlit-ready prototype for an AI journal club founded by **James Yan** and mentored by **Dr. Qingyang Xiao**.

This version combines:

1. The original Python/Streamlit AI core.
2. The dark cyan-violet neo-digital UI language from the uploaded design package.

## Main features

- Frontier AI video library and personalized recommendations
- Transparent hybrid recommender using supervised ML, TF-IDF similarity, topic fit, freshness, and feedback rewards
- AI session subscriptions
- Discussion channels and demo post creation
- High-school-level AI explanation engine
- Reinforcement-style preference updates from likes and dislikes
- Team, responsible-AI, GitHub, and Streamlit deployment pages
- Colab notebook for the AI prototype pipeline

## Project credits

- **Author and Founder:** James Yan
- **Mentor:** Dr. Qingyang Xiao

Credits appear in the sidebar, main header strip, Team tabs, and footer.

## Repository structure

```text
.
├── app.py
├── requirements.txt
├── README.md
├── ARCHITECTURE.md
├── UI_INTEGRATION.md
├── LICENSE
├── .streamlit/
│   └── config.toml
├── data/
│   ├── discussions.csv
│   ├── interactions.csv
│   ├── sessions.csv
│   ├── user_profiles.csv
│   └── videos.csv
└── notebooks/
    └── AI_Journal_Club_App_Colab.ipynb
```

## Run locally

```bash
python -m venv .venv
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a new GitHub repository.
2. Upload the **contents** of this ZIP to the repository root.
3. In Streamlit Community Cloud, create a new app from the repository.
4. Set the main file path to `app.py`.
5. Deploy.

No API key or paid service is required for this prototype.

## Prototype limitations

- Likes, subscriptions, and new posts use browser session state and reset when the session ends.
- Video links are sample search/resource links.
- The explanation engine is template-based and does not call a commercial LLM.
- A production student platform should add login, database storage, moderation, privacy controls, and human content review.
