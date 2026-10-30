import random

import streamlit as st
import joblib

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Sentiment Analysis AI | Movie Review Analyzer",
    page_icon="🎬",
    layout="wide"
)


# ==================================================
# LOAD TRAINED MODEL (unchanged)
# ==================================================

@st.cache_resource
def load_model():
    return joblib.load("logistic_regression_model.joblib")


model = load_model()


# ==================================================
# HTML HELPER
# --------------------------------------------------
# Markdown turns lines indented by 4+ spaces (and HTML
# split by blank lines) into code blocks. This helper
# strips every line and removes blank lines, so HTML
# always renders as HTML and never as visible text.
# ==================================================

def render(html: str) -> None:
    cleaned = "\n".join(
        line.strip() for line in html.splitlines() if line.strip()
    )
    st.markdown(cleaned, unsafe_allow_html=True)


# ==================================================
# SAMPLE REVIEWS (quick-try buttons, UI only)
# ==================================================

SAMPLES = {
    "positive": "An absolute masterpiece! The acting was brilliant, the story kept me hooked from the first minute, and the soundtrack gave me goosebumps. I would happily watch it again.",
    "negative": "What a disappointing waste of time. The plot made no sense, the acting was painfully wooden, and the ending was so predictable that I almost walked out of the theatre.",
}


def load_sample(kind: str) -> None:
    st.session_state["review_text"] = SAMPLES[kind]


def clear_review() -> None:
    st.session_state["review_text"] = ""


# ==================================================
# RESULT POP-UP (confetti for positive, sad red for negative)
# --------------------------------------------------
# Uses st.dialog (older Streamlit versions call it
# st.experimental_dialog). Animations are pure CSS, so
# no extra libraries are needed. This only changes how
# the result is shown; the prediction is made elsewhere.
# ==================================================

def build_confetti() -> str:
    """Party-popper style confetti shooting up from both bottom corners."""
    colors = ["#F59E0B", "#EF4444", "#22C55E", "#3B82F6",
              "#A855F7", "#EC4899", "#FACC15", "#14B8A6"]
    pieces = []
    for i in range(52):
        side = "l" if i % 2 == 0 else "r"
        direction = 1 if side == "l" else -1
        x1 = direction * random.randint(30, 200)
        y1 = -random.randint(110, 210)
        x2 = x1 + direction * random.randint(10, 70)
        y2 = random.randint(0, 40)
        rotation = random.randint(180, 900)
        delay = round(random.uniform(0, 1.2), 2)
        color = random.choice(colors)
        shape = "round" if i % 3 == 0 else ""
        pieces.append(
            f'<span class="piece {side} {shape}" style="--c:{color};'
            f'--x1:{x1}px;--y1:{y1}px;--x2:{x2}px;--y2:{y2}px;'
            f'--r:{rotation}deg;--d:{delay}s;"></span>'
        )
    return "".join(pieces)


def build_sad_rain() -> str:
    """Slowly falling broken hearts and wilted flowers."""
    icons = ["💔", "🥀", "💔", "😢"]
    drops = []
    for i in range(16):
        left = random.randint(2, 94)
        delay = round(random.uniform(0, 3), 2)
        duration = round(random.uniform(2.8, 4.5), 2)
        icon = random.choice(icons)
        drops.append(
            f'<span class="drop" style="left:{left}%;--d:{delay}s;--t:{duration}s;">{icon}</span>'
        )
    return "".join(drops)


def verdict_popup(is_positive: bool, confidence_pct: float, stars: str) -> None:
    if is_positive:
        render(f"""
<div class="pop pop-positive">
<div class="stage">
{build_confetti()}
<span class="popper pl">🎉</span>
<span class="popper pr">🎊</span>
</div>
<div class="pop-emoji bounce">😄</div>
<div class="pop-title">Positive Sentiment</div>
<div class="pop-text">Two thumbs up! 👍👍 Your review expresses a positive opinion.</div>
<span class="pop-conf">Confidence: {confidence_pct:.2f}%</span>
<div class="stars">{stars}</div>
<div class="pop-hint">Close this pop-up to see the full breakdown.</div>
</div>
""")
    else:
        render(f"""
<div class="pop pop-negative">
<div class="stage">
{build_sad_rain()}
</div>
<div class="pop-emoji sad">😢</div>
<div class="pop-title">Negative Sentiment</div>
<div class="pop-text">Thumbs down. 👎 Your review expresses a negative opinion.</div>
<span class="pop-conf">Confidence: {confidence_pct:.2f}%</span>
<div class="stars">{stars}</div>
<div class="pop-hint">Close this pop-up to see the full breakdown.</div>
</div>
""")


_dialog = getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)

if _dialog is not None:
    verdict_popup = _dialog("🎬 Audience Verdict")(verdict_popup)
else:
    # Very old Streamlit: no pop-up support, the result card below is still shown
    def verdict_popup(*args, **kwargs) -> None:
        return None


# ==================================================
# CUSTOM CSS (cinema theme)
# ==================================================

render("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Bebas+Neue&display=swap');

:root {
--bg: #0A0A14;
--card: #14141F;
--card-2: #1B1B2B;
--border: #2C2C44;
--gold: #FBBF24;
--gold-soft: #FDE68A;
--curtain: #B91C1C;
--text: #FFFFFF;
--text-soft: #D1D5DB;
--green: #22C55E;
--red: #EF4444;
}

/* Application background: dark theatre with a soft spotlight */
.stApp {
background:
radial-gradient(ellipse at 50% -10%, rgba(251, 191, 36, 0.14) 0%, rgba(10, 10, 20, 0) 55%),
radial-gradient(ellipse at 0% 100%, rgba(185, 28, 28, 0.12) 0%, rgba(10, 10, 20, 0) 50%),
#0A0A14;
color: var(--text);
font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit chrome */
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }

.block-container {
max-width: 1050px;
padding-top: 1.5rem;
padding-bottom: 3rem;
}

/* Film strip decoration */
.filmstrip {
height: 22px;
margin: 6px 0;
border-radius: 4px;
background:
repeating-linear-gradient(90deg, #0A0A14 0 14px, #E5E7EB 14px 26px, #0A0A14 26px 40px);
background-size: 40px 8px;
background-repeat: repeat-x;
background-position: 0 50%;
border-top: 6px solid #1F1F2E;
border-bottom: 6px solid #1F1F2E;
opacity: 0.85;
}

/* Hero header */
.hero {
text-align: center;
padding: 22px 10px 14px 10px;
animation: fadeIn 0.7s ease-in-out;
}
.hero-tag {
display: inline-block;
color: var(--gold);
border: 1px solid rgba(251, 191, 36, 0.5);
background: rgba(251, 191, 36, 0.08);
border-radius: 999px;
padding: 5px 16px;
font-size: 13px;
font-weight: 700;
letter-spacing: 2px;
text-transform: uppercase;
}
.hero-icons { font-size: 46px; margin: 12px 0 0 0; letter-spacing: 8px; }
.hero-title {
font-family: 'Bebas Neue', 'Inter', sans-serif;
font-size: 74px;
font-weight: 400;
letter-spacing: 4px;
line-height: 1.05;
margin: 4px 0 0 0;
background: linear-gradient(180deg, #FEF3C7 0%, #FBBF24 55%, #D97706 100%);
-webkit-background-clip: text;
background-clip: text;
-webkit-text-fill-color: transparent;
text-shadow: 0 0 40px rgba(251, 191, 36, 0.25);
}
.hero-subtitle {
color: var(--text-soft);
font-size: 18px;
font-weight: 500;
margin-top: 8px;
}

/* Generic card */
.card {
background: linear-gradient(145deg, var(--card-2), var(--card));
border: 1px solid var(--border);
border-radius: 18px;
padding: 26px;
margin: 18px 0;
animation: fadeIn 0.6s ease-in-out;
transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
}
.card:hover {
transform: translateY(-3px);
border-color: var(--gold);
box-shadow: 0 12px 32px rgba(251, 191, 36, 0.12);
}
.card h3 {
color: var(--text) !important;
font-size: 22px;
font-weight: 700;
margin: 0 0 10px 0;
}
.card p {
color: var(--text-soft) !important;
font-size: 16px;
line-height: 1.7;
margin: 0 0 8px 0;
}
.badge {
display: inline-block;
background: rgba(251, 191, 36, 0.12);
color: var(--gold-soft);
border: 1px solid rgba(251, 191, 36, 0.45);
border-radius: 999px;
padding: 5px 14px;
font-size: 14px;
font-weight: 600;
margin: 6px 6px 0 0;
}

/* Section headings with a gold marker */
.section-title {
color: var(--text);
font-size: 24px;
font-weight: 800;
margin: 32px 0 12px 0;
padding-left: 14px;
border-left: 5px solid var(--gold);
}
.section-sub {
color: var(--text-soft);
font-size: 15px;
margin: -6px 0 12px 19px;
}

/* Text area styled like a script page */
.stTextArea textarea {
background-color: #101019 !important;
color: #FFFFFF !important;
-webkit-text-fill-color: #FFFFFF !important;
border: 2px solid var(--border) !important;
border-radius: 14px !important;
font-size: 17px !important;
line-height: 1.6 !important;
padding: 16px !important;
transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
.stTextArea textarea:focus {
border-color: var(--gold) !important;
box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.25) !important;
}
.stTextArea textarea::placeholder {
color: #9CA3AF !important;
-webkit-text-fill-color: #9CA3AF !important;
opacity: 1 !important;
}

/* Stat cards (responsive grid) */
.grid {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
gap: 16px;
margin: 14px 0;
}
.stat {
background: linear-gradient(145deg, var(--card-2), var(--card));
border: 1px solid var(--border);
border-radius: 16px;
padding: 18px 20px;
text-align: center;
transition: transform 0.25s ease, border-color 0.25s ease;
}
.stat:hover { transform: translateY(-3px); border-color: var(--gold); }
.stat-label {
color: var(--text-soft);
font-size: 13px;
font-weight: 700;
text-transform: uppercase;
letter-spacing: 1px;
}
.stat-value {
color: #FFFFFF;
font-size: 32px;
font-weight: 800;
margin-top: 6px;
}
.stat-value.gold { color: var(--gold); }
.note { color: #9CA3AF; font-size: 14px; margin-top: 6px; }

/* Buttons */
.stButton > button {
border-radius: 14px !important;
font-weight: 800 !important;
font-size: 16px !important;
min-height: 52px;
transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}
.stButton > button p { font-weight: 800 !important; }

/* Primary button (Analyze) */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
background: linear-gradient(90deg, #DC2626, #F59E0B) !important;
color: #FFFFFF !important;
border: none !important;
font-size: 19px !important;
min-height: 58px;
}
.stButton > button[kind="primary"] p,
.stButton > button[data-testid="stBaseButton-primary"] p { color: #FFFFFF !important; }
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
transform: translateY(-2px);
box-shadow: 0 8px 28px rgba(245, 158, 11, 0.5);
}

/* Secondary buttons (samples, clear) */
.stButton > button[kind="secondary"],
.stButton > button[data-testid="stBaseButton-secondary"] {
background: var(--card-2) !important;
color: #FFFFFF !important;
border: 1px solid var(--border) !important;
}
.stButton > button[kind="secondary"] p,
.stButton > button[data-testid="stBaseButton-secondary"] p { color: #FFFFFF !important; }
.stButton > button[kind="secondary"]:hover,
.stButton > button[data-testid="stBaseButton-secondary"]:hover {
border-color: var(--gold) !important;
transform: translateY(-2px);
}

/* Movie ticket result card */
.ticket {
position: relative;
border-radius: 22px;
padding: 30px 24px 26px 24px;
text-align: center;
animation: fadeIn 0.6s ease-in-out;
margin: 10px 0 18px 0;
overflow: hidden;
}
.ticket::before, .ticket::after {
content: "";
position: absolute;
top: 50%;
width: 34px;
height: 34px;
border-radius: 50%;
background: #0A0A14;
transform: translateY(-50%);
}
.ticket::before { left: -17px; }
.ticket::after { right: -17px; }
.ticket-positive {
background: linear-gradient(135deg, #064E3B, #059669);
border: 2px solid #34D399;
box-shadow: 0 12px 36px rgba(34, 197, 94, 0.28);
}
.ticket-negative {
background: linear-gradient(135deg, #7F1D1D, #DC2626);
border: 2px solid #F87171;
box-shadow: 0 12px 36px rgba(239, 68, 68, 0.28);
}
.ticket-label {
color: #FFFFFF;
opacity: 0.9;
font-size: 13px;
font-weight: 700;
letter-spacing: 3px;
text-transform: uppercase;
}
.ticket-emoji { font-size: 64px; line-height: 1.15; margin-top: 6px; }
.ticket-title {
font-family: 'Bebas Neue', 'Inter', sans-serif;
color: #FFFFFF;
font-size: 48px;
letter-spacing: 3px;
margin: 4px 0 2px 0;
}
.ticket-text { color: #F9FAFB; font-size: 17px; margin: 0 0 14px 0; }
.ticket-conf {
display: inline-block;
background: rgba(0, 0, 0, 0.3);
color: #FFFFFF;
border: 1px dashed rgba(255, 255, 255, 0.6);
border-radius: 12px;
padding: 9px 24px;
font-size: 20px;
font-weight: 800;
}
.stars { font-size: 28px; letter-spacing: 4px; margin-top: 14px; color: var(--gold); }

/* Confidence and probability bars */
.bar-wrap {
background: linear-gradient(145deg, var(--card-2), var(--card));
border: 1px solid var(--border);
border-radius: 16px;
padding: 20px 22px;
margin-bottom: 14px;
}
.bar-head {
display: flex;
justify-content: space-between;
color: #FFFFFF;
font-weight: 700;
font-size: 16px;
margin-bottom: 10px;
}
.bar-track {
background: #07070E;
border-radius: 999px;
height: 18px;
overflow: hidden;
border: 1px solid var(--border);
}
.bar-fill { height: 100%; border-radius: 999px; animation: grow 1s ease-out; }
.bar-green { background: linear-gradient(90deg, #16A34A, #4ADE80); }
.bar-red { background: linear-gradient(90deg, #DC2626, #F87171); }
.bar-split { display: flex; height: 100%; }
.bar-split .pos { background: linear-gradient(90deg, #16A34A, #4ADE80); }
.bar-split .neg { background: linear-gradient(90deg, #F87171, #DC2626); }
.bar-legend {
display: flex;
justify-content: space-between;
margin-top: 10px;
font-size: 15px;
font-weight: 700;
}
.bar-legend .l-pos { color: #4ADE80; }
.bar-legend .l-neg { color: #F87171; }

/* Tech stack chips */
.chips { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
.chip {
background: var(--card-2);
color: #F3F4F6;
border: 1px solid var(--border);
border-radius: 999px;
padding: 7px 16px;
font-size: 15px;
font-weight: 600;
transition: all 0.25s ease;
}
.chip:hover {
background: var(--gold);
border-color: var(--gold);
color: #1F1300;
transform: translateY(-2px);
}

/* How-it-works steps */
.steps {
display: grid;
grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
gap: 14px;
margin-top: 8px;
}
.step {
background: #101019;
border: 1px solid var(--border);
border-radius: 14px;
padding: 16px;
text-align: center;
}
.step-icon { font-size: 30px; }
.step-title { color: #FFFFFF; font-weight: 700; margin-top: 6px; font-size: 16px; }
.step-text { color: var(--text-soft); font-size: 14px; margin-top: 4px; }

/* Alerts */
[data-testid="stAlert"] p { color: #111827 !important; font-weight: 600; }

/* Footer */
.footer {
text-align: center;
margin-top: 40px;
padding-top: 18px;
}
.footer-title {
font-family: 'Bebas Neue', 'Inter', sans-serif;
color: var(--gold);
font-size: 28px;
letter-spacing: 3px;
margin: 6px 0 0 0;
}
.footer-text { color: var(--text-soft); font-size: 14px; margin: 6px 0 0 0; }

/* ---------- Result pop-up ---------- */
div[data-testid="stDialog"] div[role="dialog"] {
background: #14141F !important;
border: 2px solid var(--gold) !important;
border-radius: 22px !important;
box-shadow: 0 20px 60px rgba(0, 0, 0, 0.7) !important;
}
div[data-testid="stDialog"] div[role="dialog"] h2,
div[data-testid="stDialog"] div[role="dialog"] h2 span {
color: #FFFFFF !important;
font-weight: 800 !important;
}
div[data-testid="stDialog"] button svg { color: #FFFFFF !important; }

.pop { text-align: center; padding: 0 6px 6px 6px; }
.pop-emoji { font-size: 86px; line-height: 1.1; margin-top: -6px; position: relative; z-index: 2; }
.pop-title {
font-family: 'Bebas Neue', 'Inter', sans-serif;
font-size: 50px;
letter-spacing: 3px;
margin: 4px 0 2px 0;
position: relative;
z-index: 2;
}
.pop-positive .pop-title { color: #4ADE80; text-shadow: 0 0 24px rgba(74, 222, 128, 0.5); }
.pop-negative .pop-title { color: #F87171; text-shadow: 0 0 24px rgba(248, 113, 113, 0.5); }
.pop-text { color: #F3F4F6; font-size: 17px; margin-bottom: 14px; position: relative; z-index: 2; }
.pop-conf {
display: inline-block;
color: #FFFFFF;
border-radius: 12px;
padding: 9px 24px;
font-size: 20px;
font-weight: 800;
position: relative;
z-index: 2;
}
.pop-positive .pop-conf { background: rgba(34, 197, 94, 0.25); border: 2px dashed #4ADE80; }
.pop-negative .pop-conf { background: rgba(239, 68, 68, 0.25); border: 2px dashed #F87171; }
.pop-hint { color: #9CA3AF; font-size: 13px; margin-top: 14px; }

/* Stage holds the confetti / sad rain */
.stage {
position: relative;
height: 210px;
margin-bottom: -70px;
overflow: hidden;
border-radius: 16px;
pointer-events: none;
}
.pop-negative .stage {
background: radial-gradient(ellipse at 50% 70%, rgba(220, 38, 38, 0.35), rgba(20, 20, 31, 0) 70%);
}

/* Cracker burst confetti */
.piece {
position: absolute;
bottom: 0;
width: 10px;
height: 16px;
background: var(--c);
opacity: 0;
animation: burst 2.6s ease-out infinite;
animation-delay: var(--d);
}
.piece.round { width: 11px; height: 11px; border-radius: 50%; }
.piece.l { left: 8%; }
.piece.r { right: 8%; }
.popper { position: absolute; bottom: 4px; font-size: 40px; animation: pop 1.3s ease-in-out infinite; }
.popper.pl { left: 3%; }
.popper.pr { right: 3%; }

@keyframes burst {
0% { transform: translate(0, 0) rotate(0deg) scale(0.4); opacity: 1; }
45% { transform: translate(var(--x1), var(--y1)) rotate(calc(var(--r) * 0.5)) scale(1); opacity: 1; }
100% { transform: translate(var(--x2), var(--y2)) rotate(var(--r)) scale(1); opacity: 0; }
}
@keyframes pop {
0%, 100% { transform: scale(1) rotate(-8deg); }
50% { transform: scale(1.25) rotate(8deg); }
}

/* Sad red rain */
.drop {
position: absolute;
top: -34px;
font-size: 24px;
opacity: 0;
animation: fall var(--t) linear infinite;
animation-delay: var(--d);
}
@keyframes fall {
0% { transform: translateY(0) rotate(-10deg); opacity: 0; }
15% { opacity: 0.95; }
100% { transform: translateY(260px) rotate(15deg); opacity: 0; }
}

/* Emoji motion */
.bounce { animation: bounce 1s ease-in-out infinite; }
.sad { animation: sadshake 2.2s ease-in-out infinite; filter: drop-shadow(0 0 18px rgba(239, 68, 68, 0.7)); }
@keyframes bounce {
0%, 100% { transform: translateY(0) scale(1); }
50% { transform: translateY(-12px) scale(1.12); }
}
@keyframes sadshake {
0%, 100% { transform: translateY(0) rotate(0deg); }
25% { transform: translateY(5px) rotate(-5deg); }
75% { transform: translateY(5px) rotate(5deg); }
}

/* Animations */
@keyframes fadeIn {
from { opacity: 0; transform: translateY(14px); }
to { opacity: 1; transform: translateY(0); }
}
@keyframes grow {
from { width: 0; }
}

/* Small screens */
@media (max-width: 640px) {
.hero-title { font-size: 46px; }
.hero-subtitle { font-size: 16px; }
.ticket-title { font-size: 36px; }
.hero-icons { font-size: 34px; }
}
</style>
""")


# ==================================================
# HEADER
# ==================================================

render("""
<div class="filmstrip"></div>
<div class="hero">
<span class="hero-tag">🎟️ Now Showing · AI Movie Review Analyzer</span>
<div class="hero-icons">🎬 🍿 🎥</div>
<h1 class="hero-title">Sentiment Analysis AI</h1>
<div class="hero-subtitle">Understand the emotions behind movie reviews using Machine Learning.</div>
</div>
<div class="filmstrip"></div>
""")


# ==================================================
# WELCOME CARD
# ==================================================

render("""
<div class="card">
<h3>🍿 Welcome to Sentiment Analysis</h3>
<p>Did the audience love the movie or hate it? Write or paste any movie review and our trained Machine Learning model will tell you whether the review is Positive or Negative, along with how confident it is.</p>
<span class="badge">TF-IDF Vectorization</span>
<span class="badge">Logistic Regression</span>
<span class="badge">Trained on IMDb Reviews</span>
</div>
""")


# ==================================================
# HOW IT WORKS
# ==================================================

render("""
<div class="steps">
<div class="step"><div class="step-icon">✍️</div><div class="step-title">1. Write</div><div class="step-text">Enter any movie review</div></div>
<div class="step"><div class="step-icon">🔠</div><div class="step-title">2. Vectorize</div><div class="step-text">TF-IDF turns words into numbers</div></div>
<div class="step"><div class="step-icon">🧠</div><div class="step-title">3. Predict</div><div class="step-text">Logistic Regression decides</div></div>
<div class="step"><div class="step-icon">🏆</div><div class="step-title">4. Verdict</div><div class="step-text">Sentiment with confidence</div></div>
</div>
""")


# ==================================================
# REVIEW INPUT
# ==================================================

render('<div class="section-title">📝 Enter Your Movie Review</div>')
render('<div class="section-sub">Type your own review, or try one of the sample reviews below.</div>')

review = st.text_area(
    "Your review",
    key="review_text",
    placeholder="Example: This movie was absolutely wonderful! The acting was brilliant and the story kept me hooked until the very end...",
    height=170,
    label_visibility="collapsed"
)

# Quick-try buttons
b1, b2, b3 = st.columns(3)
with b1:
    st.button("😊 Try a positive review", on_click=load_sample, args=("positive",), use_container_width=True)
with b2:
    st.button("😞 Try a negative review", on_click=load_sample, args=("negative",), use_container_width=True)
with b3:
    st.button("🧹 Clear", on_click=clear_review, use_container_width=True)


# ==================================================
# REVIEW STATISTICS (word and character count)
# ==================================================

word_count = len(review.split())
character_count = len(review)

render(f"""
<div class="grid">
<div class="stat">
<div class="stat-label">📝 Total Words</div>
<div class="stat-value">{word_count}</div>
</div>
<div class="stat">
<div class="stat-label">🔤 Total Characters</div>
<div class="stat-value">{character_count}</div>
</div>
</div>
""")


# ==================================================
# SENTIMENT PREDICTION (logic unchanged)
# ==================================================

if st.button("🎬 Analyze Sentiment", type="primary", use_container_width=True):

    if len(review.strip()) < 3:
        st.warning("Please enter a meaningful movie review.")

    else:
        # Predict sentiment
        prediction = model.predict([review])[0]

        # Calculate prediction probability
        probabilities = model.predict_proba([review])[0]

        classes = list(model.classes_)

        confidence = probabilities[
            classes.index(prediction)
        ]

        confidence_pct = float(confidence) * 100

        # Probability of each class (used for the audience meter)
        class_pct = {
            str(c): float(p) * 100 for c, p in zip(classes, probabilities)
        }
        positive_pct = class_pct.get("positive", confidence_pct if prediction == "positive" else 100 - confidence_pct)
        negative_pct = 100 - positive_pct

        render('<div class="section-title">🏆 The Verdict</div>')

        # Choose styling and wording based on the prediction
        if prediction == "positive":
            ticket_class = "ticket-positive"
            bar_class = "bar-green"
            emoji = "😊"
            title = "Positive Sentiment"
            message = "Two thumbs up! 👍👍 Your review expresses a positive opinion."
            explanation = (
                "The model found words and phrases in your review that are "
                "strongly associated with favourable reviews in the IMDb training data."
            )
        else:
            ticket_class = "ticket-negative"
            bar_class = "bar-red"
            emoji = "😞"
            title = "Negative Sentiment"
            message = "Thumbs down. 👎 Your review expresses a negative opinion."
            explanation = (
                "The model found words and phrases in your review that are "
                "strongly associated with unfavourable reviews in the IMDb training data."
            )

        # Star meter based on how positive the review is (UI only)
        filled = max(0, min(5, round(positive_pct / 20)))
        stars = "★" * filled + "☆" * (5 - filled)

        # Describe how sure the model is
        if confidence_pct >= 90:
            level = "The model is very confident in this prediction."
        elif confidence_pct >= 70:
            level = "The model is fairly confident in this prediction."
        else:
            level = "The model is less certain; the review may contain mixed opinions."

        # Pop-up with confetti (positive) or sad red animation (negative),
        # so the result is visible without scrolling
        verdict_popup(prediction == "positive", confidence_pct, stars)

        # Ticket-style result card
        render(f"""
<div class="ticket {ticket_class}">
<div class="ticket-label">🎟️ Audience Verdict</div>
<div class="ticket-emoji">{emoji}</div>
<div class="ticket-title">{title}</div>
<p class="ticket-text">{message}</p>
<span class="ticket-conf">Confidence: {confidence_pct:.2f}%</span>
<div class="stars">{stars}</div>
</div>
""")

        # Confidence progress bar
        render(f"""
<div class="bar-wrap">
<div class="bar-head"><span>🎯 Model Confidence</span><span>{confidence_pct:.2f}%</span></div>
<div class="bar-track"><div class="bar-fill {bar_class}" style="width:{confidence_pct:.2f}%;"></div></div>
</div>
""")

        # Positive vs negative split
        render(f"""
<div class="bar-wrap">
<div class="bar-head"><span>🎭 Positive vs Negative</span></div>
<div class="bar-track"><div class="bar-split"><div class="pos" style="width:{positive_pct:.2f}%;"></div><div class="neg" style="width:{negative_pct:.2f}%;"></div></div></div>
<div class="bar-legend"><span class="l-pos">😊 Positive {positive_pct:.2f}%</span><span class="l-neg">😞 Negative {negative_pct:.2f}%</span></div>
</div>
""")

        # Explanation card
        render(f"""
<div class="card">
<h3>💡 How to read this result</h3>
<p>{explanation}</p>
<p>{level}</p>
<div class="note">Confidence is the model's estimated probability for its predicted class. The stars show how positive the review sounds, and neither is a guarantee of correctness.</div>
</div>
""")


# ==================================================
# MODEL AND PROJECT INFORMATION
# ==================================================

render('<div class="section-title">🎞️ Behind the Scenes</div>')

render("""
<div class="grid">
<div class="stat">
<div class="stat-label">🎯 Accuracy</div>
<div class="stat-value gold">89.55%</div>
</div>
<div class="stat">
<div class="stat-label">📚 Dataset</div>
<div class="stat-value gold">50,000</div>
<div class="note">IMDb movie reviews</div>
</div>
<div class="stat">
<div class="stat-label">⚙️ Model</div>
<div class="stat-value gold" style="font-size:22px;">Logistic Regression</div>
<div class="note">with TF-IDF features</div>
</div>
</div>
""")

render("""
<div class="card">
<h3>🛠️ Technology Stack</h3>
<div class="chips">
<span class="chip">🐍 Python</span>
<span class="chip">🎈 Streamlit</span>
<span class="chip">🤖 Scikit-learn</span>
<span class="chip">🔠 TF-IDF Vectorization</span>
<span class="chip">📈 Logistic Regression</span>
<span class="chip">💾 Joblib</span>
</div>
</div>
""")


# ==================================================
# FOOTER
# ==================================================

render("""
<div class="footer">
<div class="filmstrip"></div>
<p class="footer-title">🎬 Sentiment Analysis AI</p>
<p class="footer-text">Built with Python | Scikit-learn | TF-IDF | Streamlit</p>
<p class="footer-text">Machine Learning Project · IMDb Movie Review Sentiment Classifier</p>
</div>
""")