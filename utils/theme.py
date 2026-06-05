"""
Reino Fungi & Underdark — shared visual theme for EduTrack AI.
Import UNDERDARK_CSS and inject via st.markdown(UNDERDARK_CSS, unsafe_allow_html=True).
"""

UNDERDARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Palette ─────────────────────────────────────────────────────────────────
   bg-deep      #080612   page background
   bg-surface   #120d24   cards, sidebar
   bg-elevated  #1e1438   inputs, expanders
   border       #3b1f72   card borders
   accent-v     #8b5cf6   violet — primary buttons, active
   accent-c     #22d3ee   cyan bioluminescent — highlights
   accent-f     #f97316   fungi orange — overdue, warnings
   accent-s     #c084fc   spore — secondary labels
   text-p       #ede9fe   primary text
   text-m       #a78bfa   muted text
   success      #4ade80   completed
──────────────────────────────────────────────────────────────────────────── */

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #080612;
    color: #ede9fe;
}

/* ── Sidebar ────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0920 0%, #120d24 60%, #0a1520 100%);
    border-right: 1px solid #3b1f72;
}
[data-testid="stSidebar"] * { color: #ede9fe !important; }
[data-testid="stSidebar"] .stRadio label { color: #a78bfa !important; }
[data-testid="stSidebar"] hr { border-color: #3b1f72 !important; }

/* ── Main container ─────────────────────────────────────────────────────── */
.main .block-container {
    background-color: #080612;
    padding-top: 2rem;
}

/* ── Headings ───────────────────────────────────────────────────────────── */
h1 {
    font-family: 'Cinzel', serif !important;
    color: #c084fc !important;
    text-shadow: 0 0 20px rgba(139,92,246,0.6), 0 0 40px rgba(34,211,238,0.2);
    letter-spacing: 2px;
}
h2, h3 {
    color: #ede9fe !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Cards ──────────────────────────────────────────────────────────────── */
.fungi-card {
    background: linear-gradient(135deg, #1e1438 0%, #120d24 100%);
    border: 1px solid #3b1f72;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: .75rem;
    transition: border-color .25s, box-shadow .25s;
}
.fungi-card:hover {
    border-color: #8b5cf6;
    box-shadow: 0 0 16px rgba(139,92,246,0.3);
}
.fungi-card h4 { color: #ede9fe; margin: 0 0 .3rem; font-size: 1rem; }
.fungi-card p  { color: #a78bfa; margin: 0; font-size: .85rem; }

/* ── Badges ─────────────────────────────────────────────────────────────── */
.badge-overdue  { background:#431407; color:#fb923c; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; border:1px solid #f97316; }
.badge-ok       { background:#052e16; color:#4ade80; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; border:1px solid #16a34a; }
.badge-pending  { background:#1e1438; color:#22d3ee; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; border:1px solid #0891b2; }
.badge-alta     { background:#4a0000; color:#fca5a5; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; border:1px solid #dc2626; }
.badge-media    { background:#431407; color:#fdba74; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; border:1px solid #ea580c; }
.badge-baixa    { background:#1e2a1e; color:#86efac; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; border:1px solid #16a34a; }
.badge-archived { background:#1a1a2e; color:#6366f1; border-radius:6px; padding:2px 8px; font-size:.75rem; font-weight:600; border:1px solid #4338ca; }

/* ── Metrics ────────────────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e1438, #120d24);
    border-radius: 12px;
    padding: .75rem 1rem;
    border: 1px solid #3b1f72;
    box-shadow: 0 0 12px rgba(139,92,246,0.15);
}
[data-testid="metric-container"] label { color: #a78bfa !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #c084fc !important; }

/* ── Buttons ────────────────────────────────────────────────────────────── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #6d28d9) !important;
    border: 1px solid #8b5cf6 !important;
    color: #fff !important;
    border-radius: 8px !important;
    box-shadow: 0 0 12px rgba(139,92,246,0.4) !important;
    transition: all .2s !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 24px rgba(139,92,246,0.7) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid #3b1f72 !important;
    color: #a78bfa !important;
    border-radius: 8px !important;
}

/* ── Form elements ──────────────────────────────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stDateInput > div > div > input {
    background-color: #1e1438 !important;
    border: 1px solid #3b1f72 !important;
    color: #ede9fe !important;
    border-radius: 8px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 8px rgba(139,92,246,0.4) !important;
}

/* ── Tabs ───────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #120d24 !important;
    border-bottom: 1px solid #3b1f72 !important;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #a78bfa !important;
    border-radius: 6px 6px 0 0 !important;
}
.stTabs [aria-selected="true"] {
    color: #22d3ee !important;
    border-bottom: 2px solid #22d3ee !important;
    background-color: #1e1438 !important;
}

/* ── Expander ───────────────────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background-color: #1e1438 !important;
    border: 1px solid #3b1f72 !important;
    border-radius: 8px !important;
    color: #ede9fe !important;
}
.streamlit-expanderContent {
    background-color: #120d24 !important;
    border: 1px solid #3b1f72 !important;
    border-top: none !important;
}

/* ── Alerts ─────────────────────────────────────────────────────────────── */
.stSuccess { background-color: #052e16 !important; border-left: 4px solid #4ade80 !important; }
.stError   { background-color: #2d0000 !important; border-left: 4px solid #f97316 !important; }
.stWarning { background-color: #1c1200 !important; border-left: 4px solid #eab308 !important; }
.stInfo    { background-color: #0c1a2e !important; border-left: 4px solid #22d3ee !important; }

/* ── Progress bar ───────────────────────────────────────────────────────── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #22d3ee) !important;
    box-shadow: 0 0 8px rgba(34,211,238,0.5) !important;
}

/* ── Divider ────────────────────────────────────────────────────────────── */
hr { border-color: #3b1f72 !important; }

/* ── Sidebar caption ─────────────────────────────────────────────────────── */
.stCaption { color: #6d28d9 !important; }

/* ── DataFrame ──────────────────────────────────────────────────────────── */
.stDataFrame { border: 1px solid #3b1f72 !important; border-radius: 8px !important; }
</style>
"""

# Spore glow divider HTML
SPORE_DIVIDER = """
<div style="
    height: 1px;
    background: linear-gradient(90deg, transparent, #8b5cf6, #22d3ee, #8b5cf6, transparent);
    box-shadow: 0 0 8px rgba(34,211,238,0.4);
    margin: 1.5rem 0;
"></div>
"""

PRIORITY_BADGE = {
    "alta":  '<span class="badge-alta">🔴 Alta</span>',
    "media": '<span class="badge-media">🟠 Média</span>',
    "baixa": '<span class="badge-baixa">🟢 Baixa</span>',
}

STATUS_BADGE = {
    "pending":     '<span class="badge-pending">⏳ Pendente</span>',
    "in_progress": '<span class="badge-pending">🔵 Em andamento</span>',
    "completed":   '<span class="badge-ok">✅ Concluída</span>',
}
