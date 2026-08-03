from __future__ import annotations

import html
from pathlib import Path
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.pipeline import Pipeline

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"

AUTHOR_NAME = "James Yan"
MENTOR_NAME = "Dr. Qingyang Xiao"
APP_VERSION = "v2026.08"

st.set_page_config(
    page_title="James AI Journal Club",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# UI layer adapted from the uploaded neo-digital-design concept
# -----------------------------------------------------------------------------

def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');

        :root {
            --bg: #0c1020;
            --surface: rgba(25, 31, 58, 0.72);
            --surface-2: rgba(36, 44, 80, 0.72);
            --text: #f3f7ff;
            --muted: #98a2bd;
            --cyan: #75e8ff;
            --cyan-soft: rgba(117, 232, 255, 0.18);
            --violet: #c8a4ff;
            --violet-soft: rgba(200, 164, 255, 0.16);
            --border: rgba(145, 159, 207, 0.25);
            --danger: #ff8caa;
            --success: #7ff2c2;
        }

        html, body, [class*="css"] {
            font-family: 'DM Sans', system-ui, sans-serif;
        }

        .stApp {
            color: var(--text);
            background:
                radial-gradient(1000px 560px at 8% -12%, rgba(178, 111, 255, 0.23), transparent 62%),
                radial-gradient(850px 520px at 108% 4%, rgba(66, 216, 255, 0.18), transparent 62%),
                radial-gradient(720px 520px at 52% 116%, rgba(115, 92, 255, 0.13), transparent 64%),
                linear-gradient(180deg, #0c1020 0%, #0a0e1b 100%);
            background-attachment: fixed;
        }

        .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            opacity: .32;
            background-image:
                linear-gradient(rgba(117,232,255,.055) 1px, transparent 1px),
                linear-gradient(90deg, rgba(200,164,255,.05) 1px, transparent 1px);
            background-size: 48px 48px;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,.9), rgba(0,0,0,.28));
        }

        [data-testid="stHeader"] {
            background: rgba(12, 16, 32, .34);
            backdrop-filter: blur(14px);
            border-bottom: 1px solid rgba(145,159,207,.14);
        }

        [data-testid="stToolbar"], [data-testid="stDecoration"] {
            background: transparent;
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        [data-testid="stSidebar"] {
            background: rgba(10, 14, 29, .84);
            border-right: 1px solid var(--border);
            backdrop-filter: blur(18px);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.4rem;
        }

        h1, h2, h3, h4 {
            font-family: 'Space Grotesk', system-ui, sans-serif;
            letter-spacing: -0.025em;
        }

        p, li, .stMarkdown {
            color: #d9e0f0;
        }

        code, pre, .mono, [data-testid="stCaptionContainer"] {
            font-family: 'JetBrains Mono', monospace !important;
        }

        a { color: var(--cyan); }

        .brand-wrap {
            display: flex;
            align-items: center;
            gap: .8rem;
            margin-bottom: 1rem;
        }

        .brand-mark {
            position: relative;
            width: 42px;
            height: 42px;
            display: grid;
            place-items: center;
            border: 1px solid rgba(117,232,255,.45);
            border-radius: 10px;
            color: var(--cyan);
            background: linear-gradient(135deg, rgba(117,232,255,.18), rgba(200,164,255,.17));
            box-shadow: inset 0 0 22px rgba(117,232,255,.12), 0 0 22px rgba(117,232,255,.08);
        }

        .brand-mark::before, .brand-mark::after {
            content: "";
            position: absolute;
            border-radius: 50%;
            border: 1px solid currentColor;
        }
        .brand-mark::before { width: 18px; height: 18px; opacity: .85; }
        .brand-mark::after { width: 7px; height: 7px; background: currentColor; box-shadow: 0 0 12px currentColor; }

        .brand-node {
            font-family: 'JetBrains Mono', monospace;
            font-size: 9px;
            letter-spacing: .24em;
            color: rgba(117,232,255,.78);
            text-transform: uppercase;
        }

        .brand-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.04rem;
            font-weight: 700;
            line-height: 1.15;
            background: linear-gradient(135deg, #f6fbff, var(--cyan) 48%, var(--violet));
            -webkit-background-clip: text;
            color: transparent;
        }

        .team-card, .status-card {
            padding: .9rem 1rem;
            border-radius: 10px;
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(29,36,67,.72), rgba(18,23,46,.62));
            box-shadow: inset 0 1px 0 rgba(255,255,255,.04);
        }

        .team-label, .status-label {
            font-family: 'JetBrains Mono', monospace;
            color: var(--cyan);
            font-size: 9px;
            letter-spacing: .24em;
            text-transform: uppercase;
            margin-bottom: .45rem;
        }

        .team-line {
            font-size: .79rem;
            color: #dbe4f6;
            margin: .18rem 0;
        }

        .status-dot {
            display: inline-block;
            width: 7px;
            height: 7px;
            margin-right: .45rem;
            border-radius: 999px;
            background: var(--cyan);
            box-shadow: 0 0 10px var(--cyan);
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 8px;
            padding: .55rem .7rem;
            margin: .12rem 0;
            transition: .18s ease;
            border: 1px solid transparent;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(38,47,83,.66);
            border-color: rgba(117,232,255,.18);
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(90deg, rgba(117,232,255,.12), rgba(200,164,255,.10));
            border-color: rgba(117,232,255,.24);
            box-shadow: inset 2px 0 0 var(--cyan);
        }

        [data-testid="stSidebar"] [role="radiogroup"] label p {
            font-family: 'JetBrains Mono', monospace;
            font-size: .72rem;
            letter-spacing: .06em;
        }

        .top-strip {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1.6rem;
            color: var(--muted);
            font-family: 'JetBrains Mono', monospace;
            font-size: .66rem;
            letter-spacing: .18em;
            text-transform: uppercase;
        }

        .top-strip strong { color: var(--cyan); font-weight: 500; }
        .top-strip .credits { letter-spacing: .08em; text-transform: none; }

        .page-eyebrow {
            font-family: 'JetBrains Mono', monospace;
            font-size: .7rem;
            text-transform: uppercase;
            letter-spacing: .28em;
            color: rgba(117,232,255,.84);
        }

        .page-title {
            margin: .6rem 0 .8rem;
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            line-height: 1.02;
            font-size: clamp(2.25rem, 5vw, 4.2rem);
            background: linear-gradient(135deg, #f7fbff 0%, #aef1ff 43%, #d1b5ff 78%, #eafcff 100%);
            -webkit-background-clip: text;
            color: transparent;
            text-shadow: 0 0 32px rgba(117,232,255,.08);
        }

        .page-desc {
            max-width: 820px;
            font-size: 1.04rem;
            line-height: 1.72;
            color: var(--muted);
        }

        .header-rule {
            height: 1px;
            width: 100%;
            margin: 1.4rem 0 2rem;
            background: linear-gradient(90deg, rgba(117,232,255,.7), rgba(200,164,255,.45), transparent 78%);
        }

        .metric-card {
            position: relative;
            overflow: hidden;
            min-height: 150px;
            padding: 1.2rem 1.25rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(29,36,68,.78), rgba(18,23,45,.70));
            box-shadow: inset 0 1px 0 rgba(255,255,255,.045), 0 20px 42px -30px rgba(0,0,0,.9);
        }

        .metric-card::before, .metric-card::after {
            content: "";
            position: absolute;
            width: 14px;
            height: 14px;
        }
        .metric-card::before { left: -1px; top: -1px; border-left: 1px solid var(--cyan); border-top: 1px solid var(--cyan); }
        .metric-card::after { right: -1px; bottom: -1px; border-right: 1px solid var(--violet); border-bottom: 1px solid var(--violet); }

        .metric-label {
            font-family: 'JetBrains Mono', monospace;
            color: rgba(117,232,255,.78);
            font-size: .62rem;
            letter-spacing: .22em;
            text-transform: uppercase;
        }

        .metric-value {
            margin-top: .55rem;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.75rem;
            font-weight: 700;
            line-height: 1;
            background: linear-gradient(135deg, white, var(--cyan), var(--violet));
            -webkit-background-clip: text;
            color: transparent;
        }

        .metric-rule {
            height: 1px;
            margin-top: 1rem;
            background: linear-gradient(90deg, rgba(117,232,255,.65), transparent);
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--border) !important;
            border-radius: 12px !important;
            background: linear-gradient(180deg, rgba(29,36,68,.72), rgba(17,22,43,.67)) !important;
            box-shadow: inset 0 1px 0 rgba(255,255,255,.04), 0 22px 44px -34px rgba(0,0,0,.95);
            backdrop-filter: blur(12px);
        }

        [data-testid="stVerticalBlockBorderWrapper"] > div {
            border-radius: 12px;
        }

        .section-label {
            font-family: 'JetBrains Mono', monospace;
            color: var(--cyan);
            font-size: .64rem;
            letter-spacing: .24em;
            text-transform: uppercase;
        }

        .panel-title {
            margin: .35rem 0 .65rem;
            color: var(--text);
            font-size: 1.35rem;
        }

        .chip {
            display: inline-block;
            margin: 0 .36rem .35rem 0;
            padding: .25rem .5rem;
            border-radius: 999px;
            border: 1px solid rgba(117,232,255,.28);
            color: #c8f6ff;
            background: rgba(117,232,255,.07);
            font-family: 'JetBrains Mono', monospace;
            font-size: .62rem;
        }

        .chip.violet {
            border-color: rgba(200,164,255,.32);
            color: #e4d3ff;
            background: rgba(200,164,255,.08);
        }

        .architecture {
            display: grid;
            gap: .65rem;
        }
        .arch-node {
            position: relative;
            padding: .9rem 1rem;
            border: 1px solid var(--border);
            border-radius: 9px;
            background: rgba(14,20,42,.72);
            color: #e7edf9;
            font-family: 'JetBrains Mono', monospace;
            font-size: .75rem;
            line-height: 1.55;
        }
        .arch-node strong { color: var(--cyan); }
        .arch-arrow { text-align: center; color: var(--violet); font-family: 'JetBrains Mono', monospace; }

        .concept-row {
            display: grid;
            grid-template-columns: 34px 1fr;
            gap: .8rem;
            align-items: start;
            padding: .85rem 0;
            border-bottom: 1px solid rgba(145,159,207,.14);
        }
        .concept-row:last-child { border-bottom: 0; }
        .concept-num {
            font-family: 'JetBrains Mono', monospace;
            color: var(--cyan);
            font-size: .68rem;
        }
        .concept-text { color: #d9e1f2; line-height: 1.55; }

        .content-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.25rem;
            font-weight: 650;
            color: var(--text);
            margin-bottom: .4rem;
        }
        .content-copy { color: var(--muted); line-height: 1.65; }

        .score-ring {
            width: 70px;
            height: 70px;
            display: grid;
            place-items: center;
            border-radius: 50%;
            border: 1px solid rgba(117,232,255,.45);
            background: radial-gradient(circle, rgba(117,232,255,.13), rgba(14,20,42,.8) 68%);
            box-shadow: inset 0 0 22px rgba(117,232,255,.1), 0 0 22px rgba(117,232,255,.08);
            font-family: 'Space Grotesk', sans-serif;
            font-weight: 700;
            color: var(--cyan);
        }

        .post-meta {
            color: var(--muted);
            font-family: 'JetBrains Mono', monospace;
            font-size: .66rem;
            letter-spacing: .03em;
        }

        .member-banner {
            padding: .9rem 1rem;
            border: 1px solid rgba(117,232,255,.25);
            border-radius: 10px;
            background: linear-gradient(90deg, rgba(117,232,255,.08), rgba(200,164,255,.06));
            color: #dce9fb;
        }

        .progress-row { margin: .75rem 0; }
        .progress-meta {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: .35rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: .64rem;
            color: #dbe5f7;
        }
        .progress-track {
            height: 7px;
            border-radius: 999px;
            overflow: hidden;
            background: rgba(145,159,207,.13);
        }
        .progress-fill {
            height: 100%;
            border-radius: 999px;
            background: linear-gradient(90deg, var(--cyan), var(--violet));
            box-shadow: 0 0 12px rgba(117,232,255,.35);
        }

        .role-card {
            min-height: 240px;
            padding: 1.3rem;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: linear-gradient(180deg, rgba(30,37,68,.78), rgba(16,21,42,.72));
        }
        .role-name {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            background: linear-gradient(135deg, white, var(--cyan), var(--violet));
            -webkit-background-clip: text;
            color: transparent;
        }

        .footer-note {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(145,159,207,.16);
            color: #7f89a3;
            font-family: 'JetBrains Mono', monospace;
            font-size: .63rem;
            letter-spacing: .07em;
            text-align: center;
        }

        div.stButton > button, div.stLinkButton > a, div[data-testid="stFormSubmitButton"] > button {
            border: 1px solid rgba(117,232,255,.42) !important;
            border-radius: 8px !important;
            background: rgba(117,232,255,.08) !important;
            color: #bff5ff !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: .69rem !important;
            letter-spacing: .06em !important;
            transition: .18s ease !important;
        }
        div.stButton > button:hover, div.stLinkButton > a:hover, div[data-testid="stFormSubmitButton"] > button:hover {
            border-color: var(--cyan) !important;
            background: rgba(117,232,255,.16) !important;
            box-shadow: 0 0 22px rgba(117,232,255,.14) !important;
        }

        button[kind="primary"] {
            background: linear-gradient(135deg, rgba(117,232,255,.22), rgba(200,164,255,.18)) !important;
            border-color: rgba(200,164,255,.55) !important;
        }

        [data-baseweb="select"] > div, [data-baseweb="input"] > div,
        [data-baseweb="textarea"] > div, [data-testid="stTextInputRootElement"] {
            background: rgba(18,24,48,.82) !important;
            border-color: rgba(145,159,207,.28) !important;
        }

        [data-baseweb="tab-list"] {
            gap: .35rem;
            background: transparent;
        }
        [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            font-family: 'JetBrains Mono', monospace;
            font-size: .72rem;
            color: var(--muted);
        }
        [aria-selected="true"][data-baseweb="tab"] {
            color: var(--cyan) !important;
            background: rgba(117,232,255,.07);
        }

        [data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 10px;
            overflow: hidden;
        }

        [data-testid="stAlert"] {
            border-radius: 10px;
            border: 1px solid var(--border);
            background: rgba(23,29,57,.78);
        }

        @media (max-width: 800px) {
            .block-container { padding-top: 1.2rem; }
            .top-strip { align-items: flex-start; flex-direction: column; }
            .page-title { font-size: 2.35rem; }
            .metric-card { min-height: 128px; }
            .metric-value { font-size: 2.2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Data + AI core retained from the original Streamlit prototype
# -----------------------------------------------------------------------------

@st.cache_data
def load_data() -> Dict[str, pd.DataFrame]:
    required = {
        "videos": DATA_DIR / "videos.csv",
        "sessions": DATA_DIR / "sessions.csv",
        "users": DATA_DIR / "user_profiles.csv",
        "interactions": DATA_DIR / "interactions.csv",
        "threads": DATA_DIR / "discussions.csv",
    }
    missing = [str(path.name) for path in required.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing required data file(s): {', '.join(missing)}")

    data = {name: pd.read_csv(path) for name, path in required.items()}
    data["sessions"]["date"] = pd.to_datetime(data["sessions"]["date"], errors="coerce")
    return data


def video_text(row: pd.Series) -> str:
    fields = [
        row.get("title", ""),
        row.get("topic", ""),
        row.get("level", ""),
        row.get("summary", ""),
        row.get("tags", ""),
        row.get("frontier_theme", ""),
    ]
    return " ".join(str(x) for x in fields if pd.notna(x))


def profile_text(row: pd.Series) -> str:
    fields = [
        row.get("preferred_topics", ""),
        row.get("desired_level", ""),
        f"grade {row.get('grade', '')}",
        f"math comfort {row.get('math_comfort', '')}",
        f"coding comfort {row.get('coding_comfort', '')}",
        f"time budget {row.get('time_budget_minutes', '')}",
    ]
    return " ".join(str(x) for x in fields if pd.notna(x))


def pair_text_from_merged(row: pd.Series) -> str:
    return (
        f"Member profile: {row['preferred_topics']} {row['desired_level']} "
        f"grade {row['grade']} math {row['math_comfort']} coding {row['coding_comfort']}. "
        f"Content: {row['title']} {row['topic']} {row['level']} {row['summary']} {row['tags']}"
    )


def pair_text(user_row: pd.Series, video_row: pd.Series) -> str:
    return f"Member profile: {profile_text(user_row)}. Content: {video_text(video_row)}"


@st.cache_resource
def train_supervised_model(
    users: pd.DataFrame,
    videos: pd.DataFrame,
    interactions: pd.DataFrame,
):
    merged = interactions.merge(users, on="member_id", how="left").merge(
        videos, on="content_id", how="left"
    )
    merged = merged.dropna(subset=["liked"])
    if merged.empty or merged["liked"].nunique() < 2:
        return None

    x_train = merged.apply(pair_text_from_merged, axis=1)
    y_train = merged["liked"].astype(int)
    model = Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    stop_words="english", ngram_range=(1, 2), min_df=1
                ),
            ),
            (
                "clf",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )
    model.fit(x_train, y_train)
    return model


def ensure_session_state() -> None:
    defaults = {
        "subscriptions": [],
        "new_posts": [],
        "rl_weights": {},
        "last_explanation": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def get_user_weights(user_id: str) -> Dict[str, float]:
    all_weights = st.session_state.setdefault("rl_weights", {})
    all_weights.setdefault(user_id, {})
    return all_weights[user_id]


def update_feedback(user_id: str, topic: str, reward: float) -> None:
    weights = get_user_weights(user_id)
    old = weights.get(topic, 0.0)
    weights[topic] = round(old + 0.20 * reward, 3)


def topic_match_score(preferred_topics: str, topic: str) -> float:
    preferred = [p.strip().lower() for p in str(preferred_topics).split(";")]
    return 1.0 if str(topic).strip().lower() in preferred else 0.0


def recommend_videos(
    selected_user_id: str,
    users: pd.DataFrame,
    videos: pd.DataFrame,
    interactions: pd.DataFrame,
    hide_watched: bool = True,
) -> pd.DataFrame:
    user_rows = users.loc[users["member_id"] == selected_user_id]
    if user_rows.empty:
        return pd.DataFrame()
    user_row = user_rows.iloc[0]
    model = train_supervised_model(users, videos, interactions)

    items = videos.copy()
    if hide_watched:
        watched = set(
            interactions.loc[
                (interactions["member_id"] == selected_user_id)
                & (interactions["watched"] == 1),
                "content_id",
            ]
        )
        items = items.loc[~items["content_id"].isin(watched)].copy()

    if items.empty:
        return items

    pair_texts = [pair_text(user_row, row) for _, row in items.iterrows()]
    supervised_prob = (
        np.full(len(items), 0.50)
        if model is None
        else model.predict_proba(pair_texts)[:, 1]
    )

    docs = [profile_text(user_row)] + [video_text(row) for _, row in items.iterrows()]
    vectorizer = TfidfVectorizer(stop_words="english", min_df=1)
    tfidf = vectorizer.fit_transform(docs)
    similarity = cosine_similarity(tfidf[0], tfidf[1:]).ravel()

    preferred = str(user_row["preferred_topics"])
    topic_scores = np.array(
        [topic_match_score(preferred, topic) for topic in items["topic"]]
    )
    freshness = 1.0 / (
        1.0 + (items["freshness_days"].astype(float).to_numpy() / 30.0)
    )
    weights = get_user_weights(selected_user_id)
    rl_scores = np.array(
        [np.tanh(weights.get(topic, 0.0)) for topic in items["topic"]]
    )

    items["supervised_like_probability"] = supervised_prob
    items["content_similarity"] = similarity
    items["topic_match"] = topic_scores
    items["freshness_score"] = freshness
    items["feedback_learning_score"] = rl_scores
    items["recommendation_score"] = (
        0.45 * supervised_prob
        + 0.25 * similarity
        + 0.15 * topic_scores
        + 0.10 * freshness
        + 0.05 * rl_scores
    )
    return items.sort_values("recommendation_score", ascending=False)


EXPLAINER = {
    "AI Agents": {
        "big_idea": "An AI agent is a system that can set a goal, choose steps, use tools, and check progress.",
        "analogy": "Think of it like a careful lab partner: it makes a plan, uses a calculator or search tool, and checks whether the answer makes sense.",
        "why": "Agents matter because they move AI from only answering questions toward helping complete multi-step projects.",
        "activity": "Give an agent a school-safe task, then ask it to show its plan before it takes action.",
    },
    "Deep Learning": {
        "big_idea": "Deep learning uses layers of artificial neurons to turn raw data into useful patterns.",
        "analogy": "A neural network is like a team of students passing notes: each layer adds one more clue until the final layer makes a decision.",
        "why": "It powers many frontier systems, including language models, image generators, and speech tools.",
        "activity": "Draw a three-layer network that turns study habits into a quiz-score prediction.",
    },
    "Reinforcement Learning": {
        "big_idea": "Reinforcement learning teaches an AI through rewards for good actions and penalties for bad actions.",
        "analogy": "It is like learning a video game: try a move, see the score, and improve the next move.",
        "why": "It is useful for games, robots, recommendations, and systems that improve from feedback.",
        "activity": "Design a reward rule for a robot that should reach a goal without bumping into walls.",
    },
    "Retrieval-Augmented Generation": {
        "big_idea": "RAG lets an AI look up relevant documents before it answers.",
        "analogy": "Instead of guessing from memory, the AI gets a library card and checks notes first.",
        "why": "It can reduce hallucinations and connect answers to trusted club resources.",
        "activity": "Give the AI three short paragraphs and ask it to answer only from those paragraphs.",
    },
    "AI Safety": {
        "big_idea": "AI safety asks whether a system is reliable, fair, private, and aligned with human goals.",
        "analogy": "It is like testing a bridge before people cross it: power is not enough; it must be safe.",
        "why": "Students need to understand both what AI can do and what can go wrong.",
        "activity": "For any demo, write one benefit, one risk, and one test that could catch a problem.",
    },
    "Multimodal AI": {
        "big_idea": "Multimodal AI combines different kinds of information, such as text, images, audio, and video.",
        "analogy": "It is like a student using eyes, ears, and reading notes together to understand a lesson.",
        "why": "It helps AI interact with the real world more naturally.",
        "activity": "Compare a caption written by a human with a caption generated for the same image.",
    },
    "Generative AI": {
        "big_idea": "Generative AI creates new text, images, audio, code, or video from patterns it learned.",
        "analogy": "It is like remixing many examples into a new draft, not copying one exact source.",
        "why": "It changes how people brainstorm, design, explain, and prototype ideas.",
        "activity": "Ask for three different explanations of the same idea and compare which is clearest.",
    },
    "Deployment": {
        "big_idea": "Deployment is the work of turning an AI idea into a tool people can actually use.",
        "analogy": "A science fair prototype becomes useful when it has instructions, a clean interface, and safety checks.",
        "why": "Portfolio projects need to be runnable, documented, and responsible.",
        "activity": "Turn one notebook function into a Streamlit button and test it with a friend.",
    },
}


def explain_topic(topic: str, learner_context: str = "") -> str:
    card = EXPLAINER.get(
        topic,
        {
            "big_idea": f"{topic} is an AI topic that can be understood by asking what data it uses, what pattern it learns, and how people check its output.",
            "analogy": "Imagine a new school club activity: first learn the rules, then try examples, then improve with feedback.",
            "why": "The key is to connect the advanced idea to a simple input, a process, and an output.",
            "activity": "Write one example input and one example output for this topic.",
        },
    )
    extra = (
        f"\n\nPersonal connection: Connect this topic to {learner_context.strip()}."
        if learner_context.strip()
        else ""
    )
    return (
        f"Big idea: {card['big_idea']}\n\n"
        f"High-school analogy: {card['analogy']}\n\n"
        f"Why it matters: {card['why']}\n\n"
        f"Try it in journal club: {card['activity']}"
        f"{extra}"
    )


# -----------------------------------------------------------------------------
# Presentation helpers
# -----------------------------------------------------------------------------

def safe(value: object) -> str:
    return html.escape(str(value))


def page_header(eyebrow: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="page-eyebrow">{safe(eyebrow)}</div>
        <div class="page-title">{safe(title)}</div>
        <div class="page-desc">{safe(description)}</div>
        <div class="header-rule"></div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(index: int, label: str, value: object) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{index:02d} · {safe(label)}</div>
            <div class="metric-value">{safe(value)}</div>
            <div class="metric-rule"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chips(*labels: object) -> str:
    return "".join(f'<span class="chip">{safe(label)}</span>' for label in labels)


def top_strip(page_code: str) -> None:
    st.markdown(
        f"""
        <div class="top-strip">
            <div>// {safe(page_code)} &nbsp; · &nbsp; <strong>{APP_VERSION}</strong></div>
            <div class="credits">Author: {AUTHOR_NAME} &nbsp; | &nbsp; Mentor: {MENTOR_NAME}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar() -> str:
    st.sidebar.markdown(
        """
        <div class="brand-wrap">
            <div class="brand-mark"></div>
            <div>
                <div class="brand-node">Node · JAJC-001</div>
                <div class="brand-name">James AI Journal Club</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f"""
        <div class="team-card">
            <div class="team-label">Project Credits</div>
            <div class="team-line"><strong>Author & Founder</strong><br>{AUTHOR_NAME}</div>
            <div class="team-line" style="margin-top:.55rem"><strong>Mentor</strong><br>{MENTOR_NAME}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        '<div class="section-label" style="margin:1.35rem 0 .35rem">// Explore</div>',
        unsafe_allow_html=True,
    )

    navigation = {
        "Home": "00  OVERVIEW",
        "Video Recommender": "01  RECOMMENDER",
        "Sessions": "02  SESSIONS",
        "Discussion Channels": "03  CHANNELS",
        "AI Brain Lab": "04  AI BRAIN LAB",
        "About the Team": "05  TEAM",
        "Portfolio Notes": "06  DEPLOY",
    }
    page = st.sidebar.radio(
        "Explore",
        list(navigation),
        format_func=navigation.get,
        label_visibility="collapsed",
    )
    st.sidebar.markdown(
        """
        <div class="status-card" style="margin-top:1.4rem">
            <div class="status-label">Status</div>
            <div class="team-line"><span class="status-dot"></span>Streamlit prototype online</div>
            <div class="team-line" style="color:#8d97b1;margin-top:.45rem">High-school AI learning community</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return page


def render_home(videos: pd.DataFrame, sessions: pd.DataFrame, threads: pd.DataFrame, users: pd.DataFrame) -> None:
    top_strip("system.overview")
    page_header(
        "// system.overview",
        "James AI Journal Club",
        "A future-facing learning community where students discover frontier AI videos, subscribe to tutorials, discuss ideas, and see how an AI brain personalizes learning.",
    )

    cols = st.columns(4)
    values = [
        ("Videos", len(videos)),
        ("Tutorial sessions", len(sessions)),
        ("Discussion posts", len(threads) + len(st.session_state["new_posts"])),
        ("Sample members", len(users)),
    ]
    for idx, (column, (label, value)) in enumerate(zip(cols, values), start=1):
        with column:
            metric_card(idx, label, value)

    st.write("")
    left, right = st.columns([3, 2], gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="section-label">core.mission</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">App concept</div>', unsafe_allow_html=True)
            concepts = [
                "Students watch short, current AI learning resources written at a high-school level.",
                "Members subscribe to tutorials and sessions led by James and guest mentors.",
                "Topic channels let students post questions, reactions, and project ideas.",
                "The AI brain recommends content, simplifies difficult ideas, and learns from feedback.",
            ]
            rows = "".join(
                f'<div class="concept-row"><div class="concept-num">{i:02d}</div><div class="concept-text">{safe(text)}</div></div>'
                for i, text in enumerate(concepts, start=1)
            )
            st.markdown(rows, unsafe_allow_html=True)

    with right:
        with st.container(border=True):
            st.markdown('<div class="section-label">brain.pipeline</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">AI architecture</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="architecture">
                    <div class="arch-node"><strong>01 · INPUT</strong><br>Open resources + club videos + survey profiles</div>
                    <div class="arch-arrow">↓</div>
                    <div class="arch-node"><strong>02 · PREDICT</strong><br>Supervised ML recommendation model</div>
                    <div class="arch-arrow">↓</div>
                    <div class="arch-node"><strong>03 · EXPLAIN</strong><br>High-school explanation + concept layer</div>
                    <div class="arch-arrow">↓</div>
                    <div class="arch-node"><strong>04 · LEARN</strong><br>Reward updates from likes, skips, and subscriptions</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    with st.container(border=True):
        st.markdown('<div class="section-label">club.signal</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Built for exploration, not passive scrolling</div>', unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            st.markdown("**Discover**")
            st.write("Curated resources connect frontier research with accessible explanations.")
        with b:
            st.markdown("**Discuss**")
            st.write("Channels help members question claims, compare ideas, and propose experiments.")
        with c:
            st.markdown("**Build**")
            st.write("Notebook and Streamlit components turn learning into a working portfolio project.")


def render_recommender(users: pd.DataFrame, videos: pd.DataFrame, interactions: pd.DataFrame) -> None:
    top_strip("recommender.engine")
    page_header(
        "// 01 · recommender.engine",
        "Personalized Frontier AI Videos",
        "A transparent hybrid recommender combines supervised learning, profile similarity, topic fit, freshness, and feedback rewards.",
    )

    c1, c2 = st.columns([2, 1])
    with c1:
        labels = users.apply(
            lambda r: f"{r['member_id']} · {r['name']} · Grade {r['grade']}", axis=1
        ).tolist()
        user_label = st.selectbox("Sample member profile", labels)
    with c2:
        hide_watched = st.toggle("Hide watched videos", value=True)

    user_id = user_label.split(" · ")[0]
    selected_user = users.loc[users["member_id"] == user_id].iloc[0]
    recs = recommend_videos(user_id, users, videos, interactions, hide_watched)

    st.markdown(
        f"""
        <div class="member-banner">
            <strong>{safe(selected_user['name'])}</strong> · Grade {safe(selected_user['grade'])}<br>
            {chips('Topics: ' + str(selected_user['preferred_topics']), 'Level: ' + str(selected_user['desired_level']), 'Time: ' + str(selected_user['time_budget_minutes']) + ' min')}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    if recs.empty:
        st.warning("No recommendations remain after filtering. Turn off the watched-video filter to see the complete library.")
        return

    for rank, (_, row) in enumerate(recs.head(6).iterrows(), start=1):
        with st.container(border=True):
            main_col, score_col = st.columns([6, 1])
            with main_col:
                st.markdown(
                    f'<div class="section-label">rank.{rank:02d} · {safe(row["frontier_theme"])}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="content-title">{safe(row["title"])}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="content-copy">{safe(row["summary"])}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    chips(
                        row["topic"],
                        row["level"],
                        f"{row['estimated_minutes']} min",
                        row["format"],
                    ),
                    unsafe_allow_html=True,
                )
            with score_col:
                score = int(round(float(row["recommendation_score"]) * 100))
                st.markdown(f'<div class="score-ring">{score}</div>', unsafe_allow_html=True)

            action1, action2, action3, action4 = st.columns([1.4, 1, 1.2, 2.4])
            with action1:
                st.link_button("OPEN RESOURCE", str(row["source_url"]), use_container_width=True)
            with action2:
                if st.button("LIKE +", key=f"like_{user_id}_{row['content_id']}", use_container_width=True):
                    update_feedback(user_id, str(row["topic"]), 1.0)
                    st.toast("Positive reward saved. Topic weight increased.", icon="✅")
                    st.rerun()
            with action3:
                if st.button("NOT FOR ME", key=f"dislike_{user_id}_{row['content_id']}", use_container_width=True):
                    update_feedback(user_id, str(row["topic"]), -1.0)
                    st.toast("Negative reward saved. Topic weight decreased.", icon="↘️")
                    st.rerun()
            with action4:
                with st.expander("WHY THIS MATCHED"):
                    st.write(f"Supervised like probability: **{row['supervised_like_probability']:.2f}**")
                    st.write(f"Profile-content similarity: **{row['content_similarity']:.2f}**")
                    st.write(f"Topic match: **{row['topic_match']:.2f}**")
                    st.write(f"Freshness score: **{row['freshness_score']:.2f}**")
                    st.write(f"Feedback learning score: **{row['feedback_learning_score']:.2f}**")

    st.write("")
    with st.expander("MODEL TRANSPARENCY TABLE"):
        display = recs[
            [
                "title",
                "topic",
                "supervised_like_probability",
                "content_similarity",
                "topic_match",
                "freshness_score",
                "feedback_learning_score",
                "recommendation_score",
            ]
        ].head(10).copy()
        numeric_cols = display.select_dtypes(include="number").columns
        display[numeric_cols] = display[numeric_cols].round(3)
        st.dataframe(display, use_container_width=True, hide_index=True)
        st.caption("Prototype scoring formula: 45% supervised probability + 25% similarity + 15% topic match + 10% freshness + 5% feedback reward.")


def render_sessions(sessions: pd.DataFrame) -> None:
    top_strip("sessions.registry")
    page_header(
        "// 02 · sessions.registry",
        "AI Sessions & Tutorials",
        "Browse workshops, reserve a place, and assemble a personalized learning sequence for the journal club.",
    )

    f1, f2 = st.columns([2, 1])
    topics = ["All"] + sorted(sessions["topic"].dropna().unique().tolist())
    with f1:
        topic_filter = st.selectbox("Topic filter", topics)
    with f2:
        difficulty = st.selectbox(
            "Difficulty",
            ["All"] + sorted(sessions["difficulty"].dropna().unique().tolist()),
        )

    shown = sessions.copy()
    if topic_filter != "All":
        shown = shown.loc[shown["topic"] == topic_filter]
    if difficulty != "All":
        shown = shown.loc[shown["difficulty"] == difficulty]

    for _, row in shown.sort_values("date").iterrows():
        subscribed = row["session_id"] in st.session_state["subscriptions"]
        with st.container(border=True):
            left, right = st.columns([5, 1.4])
            with left:
                date_text = row["date"].strftime("%b %d, %Y") if pd.notna(row["date"]) else "Date TBA"
                st.markdown(
                    f'<div class="section-label">{safe(row["session_id"])} · {safe(date_text)}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f'<div class="content-title">{safe(row["title"])}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="content-copy">{safe(row["description"])}</div>', unsafe_allow_html=True)
                st.markdown(
                    chips(row["topic"], row["difficulty"], f"Teacher: {row['teacher']}", f"Capacity: {row['capacity']}"),
                    unsafe_allow_html=True,
                )
            with right:
                st.markdown(
                    f'<div class="score-ring" style="font-size:.76rem;text-align:center">{"JOINED" if subscribed else "OPEN"}</div>',
                    unsafe_allow_html=True,
                )
                if subscribed:
                    if st.button("UNSUBSCRIBE", key=f"unsub_{row['session_id']}", use_container_width=True):
                        st.session_state["subscriptions"].remove(row["session_id"])
                        st.rerun()
                else:
                    if st.button("SUBSCRIBE", key=f"sub_{row['session_id']}", type="primary", use_container_width=True):
                        st.session_state["subscriptions"].append(row["session_id"])
                        st.toast("Session added to your demo learning plan.", icon="📡")
                        st.rerun()

    st.write("")
    with st.container(border=True):
        st.markdown('<div class="section-label">member.schedule</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">My demo subscriptions</div>', unsafe_allow_html=True)
        subscribed_df = sessions.loc[
            sessions["session_id"].isin(st.session_state["subscriptions"])
        ]
        if subscribed_df.empty:
            st.write("No sessions selected yet. Subscribe above to build a learning path.")
        else:
            st.dataframe(
                subscribed_df[["date", "title", "topic", "difficulty", "teacher"]].sort_values("date"),
                hide_index=True,
                use_container_width=True,
            )


def render_discussions(threads: pd.DataFrame) -> None:
    top_strip("channels.network")
    page_header(
        "// 03 · channels.network",
        "Discussion Channels",
        "A student-centered space for questions, reactions, journal-club notes, project ideas, and responsible debate.",
    )

    all_threads = threads.copy()
    if st.session_state["new_posts"]:
        all_threads = pd.concat(
            [all_threads, pd.DataFrame(st.session_state["new_posts"])],
            ignore_index=True,
        )

    c1, c2 = st.columns([2, 1])
    with c1:
        channel = st.selectbox(
            "Channel",
            ["All"] + sorted(all_threads["channel"].dropna().unique().tolist()),
        )
    with c2:
        sort_order = st.selectbox("Sort", ["Newest", "Most upvoted"])

    shown = all_threads if channel == "All" else all_threads.loc[all_threads["channel"] == channel]
    shown = shown.sort_values("upvotes" if sort_order == "Most upvoted" else "timestamp", ascending=False)

    feed, composer = st.columns([3, 2], gap="large")
    with feed:
        for _, row in shown.iterrows():
            with st.container(border=True):
                st.markdown(
                    f'<div class="section-label">#{safe(row["channel"])} · {safe(row["topic"])}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(f'<div class="content-copy" style="font-size:1rem">{safe(row["post"])}</div>', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="post-meta">By {safe(row["author"])} · {safe(row["timestamp"])} · ▲ {safe(row["upvotes"])}</div>',
                    unsafe_allow_html=True,
                )

    with composer:
        with st.container(border=True):
            st.markdown('<div class="section-label">compose.message</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Add a demo post</div>', unsafe_allow_html=True)
            with st.form("new_post_form", clear_on_submit=True):
                author = st.text_input("Name", value="New Member")
                channel_name = st.text_input("Channel", value="ai-brain-ideas")
                topic_name = st.text_input("Topic", value="AI Agents")
                post = st.text_area(
                    "Post",
                    value="How can we test whether an AI recommendation is genuinely helpful?",
                    height=150,
                )
                submitted = st.form_submit_button("TRANSMIT POST", use_container_width=True)
            if submitted and post.strip():
                st.session_state["new_posts"].append(
                    {
                        "thread_id": f"NEW{len(st.session_state['new_posts']) + 1:03d}",
                        "channel": channel_name.strip() or "general",
                        "author": author.strip() or "New Member",
                        "topic": topic_name.strip() or "AI",
                        "post": post.strip(),
                        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
                        "upvotes": 0,
                    }
                )
                st.toast("Post added to this browser session.", icon="💬")
                st.rerun()

            st.caption("Demo posts live only in Streamlit session state. Production deployment should use authentication, moderation, and a database.")


def render_ai_brain(users: pd.DataFrame) -> None:
    top_strip("brain.interface")
    page_header(
        "// 04 · brain.interface",
        "AI Brain Lab",
        "Translate advanced AI ideas into high-school language, inspect the three-layer architecture, and observe feedback-driven preference updates.",
    )

    explainer_col, architecture_col = st.columns([3, 2], gap="large")
    with explainer_col:
        with st.container(border=True):
            st.markdown('<div class="section-label">concept.translator</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">High-school explanation engine</div>', unsafe_allow_html=True)
            topic = st.selectbox("AI topic", sorted(EXPLAINER.keys()))
            learner_context = st.text_area(
                "Optional learner context",
                placeholder="Example: I like biology, robotics, or science fair projects.",
            )
            if st.button("▶ EXPLAIN IT SIMPLY", type="primary"):
                st.session_state["last_explanation"] = explain_topic(topic, learner_context)
            if st.session_state["last_explanation"]:
                st.markdown('<div class="section-label" style="margin-top:1rem">output.stream</div>', unsafe_allow_html=True)
                st.info(st.session_state["last_explanation"])

    with architecture_col:
        with st.container(border=True):
            st.markdown('<div class="section-label">model.layers</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Three AI layers</div>', unsafe_allow_html=True)
            layers = [
                ("01", "Supervised ML", "Learns from surveys, watch history, and likes to predict useful videos."),
                ("02", "Concept layer", "Represents complex AI topics through structured analogies and activities."),
                ("03", "Reward feedback", "Updates topic weights when students like or reject content."),
            ]
            for number, title, description in layers:
                st.markdown(
                    f"""
                    <div class="concept-row">
                        <div class="concept-num">{number}</div>
                        <div><strong>{safe(title)}</strong><br><span style="color:#98a2bd">{safe(description)}</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with st.container(border=True):
            st.markdown('<div class="section-label">feedback.weights</div>', unsafe_allow_html=True)
            user_for_weights = st.selectbox(
                "Member",
                users.apply(lambda r: f"{r['member_id']} · {r['name']}", axis=1).tolist(),
                key="weights_user",
            )
            weights = get_user_weights(user_for_weights.split(" · ")[0])
            if not weights:
                st.write("No feedback recorded yet. Use the Like or Not for me buttons in the recommender.")
            else:
                max_abs = max(0.2, max(abs(v) for v in weights.values()))
                bars = ""
                for topic_name, weight in sorted(weights.items(), key=lambda item: -item[1]):
                    width = max(3, min(100, 50 + (weight / max_abs) * 50))
                    bars += (
                        '<div class="progress-row">'
                        f'<div class="progress-meta"><span>{safe(topic_name)}</span><span>{weight:+.2f}</span></div>'
                        f'<div class="progress-track"><div class="progress-fill" style="width:{width:.1f}%"></div></div>'
                        '</div>'
                    )
                st.markdown(bars, unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown('<div class="section-label">responsible.ai</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Responsible AI checklist</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.checkbox("Show why each recommendation was made.", value=True)
            st.checkbox("Let students control interests and clear feedback.", value=True)
        with c2:
            st.checkbox("Use human review before publishing official content.", value=True)
            st.checkbox("Avoid collecting sensitive personal data from minors.", value=True)


def render_team() -> None:
    top_strip("team.directory")
    page_header(
        "// 05 · team.directory",
        "Meet the Project Team",
        "The AI Journal Club combines student leadership with technical mentoring to make frontier AI understandable, responsible, and portfolio-ready.",
    )

    mission_tab, author_tab, mentor_tab = st.tabs(
        ["PROJECT MISSION", f"AUTHOR · {AUTHOR_NAME}", f"MENTOR · {MENTOR_NAME}"]
    )
    with mission_tab:
        with st.container(border=True):
            st.markdown('<div class="section-label">mission.statement</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">A student-centered frontier AI community</div>', unsafe_allow_html=True)
            st.write(
                "Members discover current AI resources, subscribe to tutorials, exchange ideas, and learn how machine learning, deep learning, and feedback-driven personalization work. The prototype is designed to become both a club platform and a public technical portfolio."
            )
            st.markdown(chips("Accessible AI", "Student leadership", "Responsible design", "Open portfolio"), unsafe_allow_html=True)

    with author_tab:
        st.markdown(
            f"""
            <div class="role-card">
                <div class="section-label">author.founder</div>
                <div class="role-name">{AUTHOR_NAME}</div>
                <p>James Yan founded the AI Journal Club and leads its mission to make frontier AI ideas understandable, engaging, and useful for high-school students.</p>
                <p><strong>Focus:</strong> journal-club vision, student community, content direction, session planning, and portfolio ownership.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with mentor_tab:
        st.markdown(
            f"""
            <div class="role-card">
                <div class="section-label">technical.mentor</div>
                <div class="role-name">{MENTOR_NAME}</div>
                <p>Dr. Qingyang Xiao mentors the project architecture, AI prototyping, data-driven recommendation design, responsible-AI planning, and portfolio development.</p>
                <p><strong>Focus:</strong> AI architecture, prototype implementation, model transparency, deployment guidance, and technical review.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_portfolio() -> None:
    top_strip("deploy.manifest")
    page_header(
        "// 06 · deploy.manifest",
        "GitHub & Streamlit Portfolio Notes",
        "A clean deployment manifest for publishing the integrated prototype as James's GitHub portfolio project.",
    )

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="section-label">manifest.repo</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Suggested repository</div>', unsafe_allow_html=True)
            st.code("ai-journal-club-app", language="text")
            st.markdown("**Local launch**")
            st.code("pip install -r requirements.txt\nstreamlit run app.py", language="bash")

    with right:
        with st.container(border=True):
            st.markdown('<div class="section-label">deploy.sequence</div>', unsafe_allow_html=True)
            st.markdown('<div class="panel-title">Streamlit Community Cloud</div>', unsafe_allow_html=True)
            steps = [
                "Create a GitHub repository.",
                "Upload the contents of this ZIP to the repository root.",
                "Commit app.py, requirements.txt, data/, notebooks/, and .streamlit/.",
                "In Streamlit Community Cloud, select the repository and set app.py as the main file.",
            ]
            rows = "".join(
                f'<div class="concept-row"><div class="concept-num">{i:02d}</div><div class="concept-text">{safe(step)}</div></div>'
                for i, step in enumerate(steps, start=1)
            )
            st.markdown(rows, unsafe_allow_html=True)

    st.write("")
    with st.container(border=True):
        st.markdown('<div class="section-label">upgrade.queue</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Production upgrade path</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("- Replace sample resources with club-curated links.\n- Add secure sign-in and persistent profiles.\n- Connect a database for posts and subscriptions.")
        with c2:
            st.markdown("- Add teacher moderation and content review.\n- Add retrieval over approved club notes.\n- Add privacy controls and data deletion.")


def main() -> None:
    inject_css()
    ensure_session_state()

    try:
        data = load_data()
    except Exception as exc:
        st.error(f"The app could not load its data: {exc}")
        st.stop()

    page = sidebar()
    if page == "Home":
        render_home(data["videos"], data["sessions"], data["threads"], data["users"])
    elif page == "Video Recommender":
        render_recommender(data["users"], data["videos"], data["interactions"])
    elif page == "Sessions":
        render_sessions(data["sessions"])
    elif page == "Discussion Channels":
        render_discussions(data["threads"])
    elif page == "AI Brain Lab":
        render_ai_brain(data["users"])
    elif page == "About the Team":
        render_team()
    elif page == "Portfolio Notes":
        render_portfolio()

    st.markdown(
        f'<div class="footer-note">JAMES AI JOURNAL CLUB · AUTHOR {AUTHOR_NAME.upper()} · MENTOR {MENTOR_NAME.upper()} · {APP_VERSION}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
