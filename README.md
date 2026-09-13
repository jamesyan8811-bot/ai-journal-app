# James AI Journal Club App

A complete GitHub- and Streamlit-ready AI journal club prototype founded by **James Yan** and mentored by **Dr. Qingyang Xiao**.

This build combines the working Python AI core with the uploaded **neo-digital-design** UI source. The Streamlit interface now follows the source design's dark black-and-emerald visual system, glass panels, ambient grid, animated scanline, code-style labels, glowing navigation, responsive cards, and gradient typography.

## Live project links

- GitHub repository: `https://github.com/qxiao2ub/ai-journal-club-app`
- Streamlit app: `https://ai-journal-club.streamlit.app/`

## Main features

- Curated frontier-AI video library for high-school learners
- Transparent hybrid video recommender
- Supervised machine learning using TF-IDF and logistic regression
- Profile and content similarity scoring
- Topic-match and content-freshness scoring
- Reinforcement-style preference updates from likes and dislikes
- AI tutorial and session subscriptions
- Discussion channels with session-based demo posting
- High-school-level AI explanation engine
- Responsible-AI checklist and model-transparency table
- Team and portfolio pages with author and mentor credits
- Google Colab notebook containing the AI prototype pipeline

## Project credits

- **Author and Founder:** James Yan
- **Mentor:** Dr. Qingyang Xiao

Credits are displayed in the sidebar, top project strip, Team tabs, Portfolio page, and footer.

## Repository structure

```text
.
├── app.py                         # Streamlit Community Cloud entry point
├── requirements.txt              # Python dependencies
├── README.md
├── ARCHITECTURE.md
├── UI_INTEGRATION.md
├── LICENSE
├── .streamlit/
│   └── config.toml               # Matching dark emerald Streamlit theme
├── data/
│   ├── discussions.csv
│   ├── interactions.csv
│   ├── sessions.csv
│   ├── user_profiles.csv
│   └── videos.csv
├── notebooks/
│   └── AI_Journal_Club_App_Colab.ipynb
└── ui_reference/
    ├── README.md
    └── neo-digital-design-main/  # Original uploaded React/Vite UI source
```

The files in `ui_reference/` are retained for design provenance and James's portfolio. Streamlit does not need Node.js or Bun at runtime; the visual language has been ported into `app.py`.

## Run locally

Create and activate a Python environment, then run:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Windows PowerShell example:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create or open the GitHub repository.
2. Upload the **contents inside this ZIP** to the repository root.
3. Commit and push all files.
4. In Streamlit Community Cloud, create an app from the repository.
5. Set the main file path to `app.py`.
6. Deploy or reboot the existing app.

No API key or paid service is required for this prototype.

## UI integration and header protection

This build ports the uploaded UI's updated emerald palette and visual components into native Streamlit CSS and widgets. It also preserves a toolbar-safe top offset of `5rem` on desktop and `4.5rem` on smaller screens, so the Streamlit toolbar does not cover the top project-status line.

## Prototype limitations

- Likes, subscriptions, and newly created posts are stored in Streamlit session state and reset when the browser session ends.
- Resource links and datasets are demonstration content and should be reviewed by the club before public use.
- The explanation engine is template-based and does not call a paid language-model API.
- A production platform for minors should add authentication, database persistence, moderation, privacy controls, consent workflows, and human review.
