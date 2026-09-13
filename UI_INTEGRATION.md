# Neo-Digital UI Integration Notes

## Integrated source

The repository includes and adapts the uploaded UI package:

```text
neo-digital-design-main (1) (1).zip
```

The original React/Vite source is retained under:

```text
ui_reference/neo-digital-design-main/
```

## How the integration works

The uploaded UI is a TypeScript React design, while the deployable application is a Python Streamlit app. Its visual system was therefore ported rather than requiring a separate Node server. The working AI features remain in `app.py`, and the source UI is included as a portfolio and design reference.

## Visual components ported to Streamlit

- Near-black, green-tinted background based on the source OKLCH tokens
- Emerald primary and secondary glow system
- Fixed 48-pixel ambient grid
- Animated horizontal scanline
- Glass-style panels and cards
- Corner brackets and glowing card edges
- Space Grotesk, DM Sans, and JetBrains Mono typography
- Code-style page labels and numbered navigation
- Gradient titles and metrics
- Styled buttons, form controls, tabs, alerts, tables, and progress indicators
- Responsive desktop and mobile spacing
- Branded sidebar with author, mentor, GitHub, and live-app links

## Functional core retained

- CSV-backed videos, sessions, users, interactions, and discussions
- Supervised TF-IDF plus logistic-regression recommendation model
- Profile/content cosine similarity
- Topic-fit and freshness scoring
- Feedback-driven topic weights
- Session subscriptions
- Discussion posting in session state
- High-school-level AI explanation engine
- Model transparency output
- Responsible-AI checklist
- Google Colab notebook

## Streamlit deployment entry point

```text
app.py
```

Node.js and Bun are not required by Streamlit Community Cloud because `ui_reference/` is not the runtime front end.

## Streamlit toolbar compatibility

The app keeps a `5rem` desktop and `4.5rem` mobile top offset. This prevents Streamlit's fixed toolbar from hiding the top system-status and project-credit line.
