CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0d0d1a !important;
    color: #e0e0f0;
}

.stApp { background: #0d0d1a; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #12121f !important;
    border-right: 0.5px solid #1e1e35;
}
[data-testid="stSidebar"] * { color: #c0c0d8 !important; }

/* ── Cards ── */
.morphui-card {
    background: #12121f;
    border: 0.5px solid #1e1e35;
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 14px;
    transition: border-color 0.2s ease, transform 0.2s ease;
}
.morphui-card:hover {
    border-color: #2e2e50;
    transform: translateY(-1px);
}

/* ── Animate In ── */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.animate-in {
    animation: fadeSlideUp 0.45s ease forwards;
}

/* ── Typography ── */
.card-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #5a5a7a;
    margin-bottom: 10px;
}
.metric-value {
    font-size: 32px;
    font-weight: 700;
    font-family: 'Syne', sans-serif;
    line-height: 1.1;
    margin-bottom: 4px;
}
.metric-label { font-size: 13px; color: #5a5a7a; }
.metric-delta { font-size: 12px; margin-top: 6px; font-family: 'DM Mono', monospace; }
.text-content { font-size: 14px; color: #a0a0c0; line-height: 1.7; }

/* ── Tags ── */
.tags-wrap { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 4px; }
.tag {
    font-size: 11px;
    font-family: 'DM Mono', monospace;
    padding: 4px 10px;
    border-radius: 20px;
    font-weight: 500;
}

/* ── Progress ── */
.progress-item { margin-bottom: 12px; }
.progress-label-row {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: #a0a0c0;
    margin-bottom: 5px;
    font-family: 'DM Mono', monospace;
}
.progress-track {
    background: #1e1e35;
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 1s ease;
}

/* ── SWOT ── */
.swot-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin-top: 8px;
}
.swot-quad {
    background: #0d0d1a;
    border-radius: 8px;
    padding: 12px;
    padding-top: 14px;
}
.swot-title {
    font-size: 11px;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.swot-list {
    padding-left: 14px;
    color: #a0a0c0;
    font-size: 12px;
    line-height: 1.8;
}

/* ── Page Header ── */
.morphui-header {
    text-align: center;
    padding: 2rem 0 1.5rem;
    border-bottom: 0.5px solid #1e1e35;
    margin-bottom: 2rem;
}
.morphui-logo {
    font-size: 36px;
    font-weight: 700;
    background: linear-gradient(135deg, #4a9eff, #00d4aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.02em;
}
.morphui-tagline {
    font-size: 13px;
    color: #5a5a7a;
    font-family: 'DM Mono', monospace;
    margin-top: 4px;
}
.result-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 4px;
}
.result-subtitle {
    font-size: 13px;
    color: #5a5a7a;
    font-family: 'DM Mono', monospace;
    margin-bottom: 1.5rem;
}

/* ── Streaming indicator ── */
.streaming-indicator {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #4a9eff;
    padding: 8px 12px;
    background: #4a9eff11;
    border-radius: 6px;
    border: 0.5px solid #4a9eff33;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4a9eff22, #00d4aa22) !important;
    border: 0.5px solid #4a9eff55 !important;
    color: #e0e0f0 !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    letter-spacing: 0.05em !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #4a9eff44, #00d4aa44) !important;
    border-color: #4a9eff !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ── */
.stTextArea textarea, .stTextInput input {
    background: #12121f !important;
    border: 0.5px solid #1e1e35 !important;
    border-radius: 8px !important;
    color: #e0e0f0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d0d1a; }
::-webkit-scrollbar-thumb { background: #2a2a40; border-radius: 4px; }

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* Dark dataframe */
[data-testid="stDataFrame"] iframe {
    background: #12121f !important;
    color: #e0e0f0 !important;
}
/* ── Selectbox ── */
div[data-baseweb="select"] > div {
    background: #12121f !important;
    border-color: #1e1e35 !important;
}
div[data-baseweb="select"] span {
    color: #e0e0f0 !important;
}
div[data-baseweb="select"] input {
    color: #e0e0f0 !important;
}
/* ── Force sidebar visible ── */
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
    width: 300px !important;
    transform: translateX(0) !important;
    background: #12121f !important;
    border-right: 0.5px solid #1e1e35 !important;
}
[data-testid="collapsedControl"] {
    display: none !important;
}
</style>
"""