import streamlit as st
import time

# --- EXTREME UI EXTRAS: GOOGLE FONTS & ADVANCED CSS ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap" rel="stylesheet">
<style>
    /* Premium Typography - Robust Fix for Icon Glitch */
    html, body, [class*="st-"]:not(.material-icons):not(.material-symbols-outlined):not(i):not(svg) {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Ensure Streamlit Icons (Material Icons) are NOT overridden */
    .material-icons, 
    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined', 'Material Icons' !important;
        font-feature-settings: 'liga' !important;
    }

    /* Sidebar user content spacing */
    [data-testid="stSidebarUserContent"] {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Animated Mesh Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(0, 201, 255, 0.05) 0%, transparent 40%),
                    radial-gradient(circle at 90% 80%, rgba(146, 254, 157, 0.05) 0%, transparent 40%);
        background-color: #0E1117;
    }

    /* Staggered Card Entrances */
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .card-1 { animation: slideInUp 0.6s ease-out forwards; }
    .card-2 { animation: slideInUp 0.6s ease-out 0.2s forwards; opacity: 0; }
    
    /* Typewriter Effect Animation */
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    .typewriter h3 {
        overflow: hidden;
        border-right: .15em solid orange;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        animation: 
            typing 3.5s steps(40, end),
            blink-caret .75s step-end infinite;
    }
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: orange; }
    }

    /* Glassmorphism Refinement */
    .stColumn > div > div > div {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
        border-radius: 20px !important;
    }

    /* Button Pulse Glow */
    .stButton > button {
        transition: all 0.3s ease;
        border: 1px solid rgba(0, 201, 255, 0.3) !important;
    }
    .stButton > button:hover {
        box-shadow: 0 0 15px rgba(0, 201, 255, 0.4);
        border: 1px solid rgba(0, 201, 255, 0.8) !important;
        transform: scale(1.02);
    }

    /* Gradient Title */
    .gradient-text {
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3.5rem;
        letter-spacing: -1px;
    }

    /* Floating Profile Pic */
    [data-testid="stSidebar"] img {
        border: 3px solid rgba(0, 201, 255, 0.2);
        padding: 5px;
        border-radius: 50%;
        animation: float 4s ease-in-out infinite;
    }
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    /* ── Gradient Divider ── */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #00C9FF, #92FE9D, transparent);
        border: none;
        margin: 1.5rem 0;
        animation: shimmer 3s ease-in-out infinite;
    }
    @keyframes shimmer {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }

    /* ── Page Link Hover Cards ── */
    [data-testid="stPageLink"] {
        transition: all 0.25s ease !important;
        border-radius: 8px !important;
    }
    [data-testid="stPageLink"]:hover {
        background: rgba(0, 201, 255, 0.06) !important;
        transform: translateX(4px);
        box-shadow: -3px 0 0 0 #00C9FF;
    }

    /* ── Stagger the nav cards on About page ── */
    .card-1 [data-testid="stPageLink"]:nth-child(1) { animation: slideInUp 0.4s ease-out 0.1s both; }
    .card-1 [data-testid="stPageLink"]:nth-child(2) { animation: slideInUp 0.4s ease-out 0.2s both; }
    .card-1 [data-testid="stPageLink"]:nth-child(3) { animation: slideInUp 0.4s ease-out 0.3s both; }
    .card-1 [data-testid="stPageLink"]:nth-child(4) { animation: slideInUp 0.4s ease-out 0.4s both; }
    .card-2 [data-testid="stPageLink"]:nth-child(1) { animation: slideInUp 0.4s ease-out 0.3s both; }
    .card-2 [data-testid="stPageLink"]:nth-child(2) { animation: slideInUp 0.4s ease-out 0.4s both; }
    .card-2 [data-testid="stPageLink"]:nth-child(3) { animation: slideInUp 0.4s ease-out 0.5s both; }

    /* ── Subtle gradient text for subheaders ── */
    .explore-heading {
        background: linear-gradient(135deg, #00C9FF 30%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.4rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Sequential Content Loading
st.markdown('<h1 class="gradient-text">🚀 Optimization Portfolio</h1>', unsafe_allow_html=True)

# Typewriter Intro
st.markdown(f"""
<div class="typewriter">
    <h3 style="color: #92FE9D; font-size: 1.2rem;">Rizwan — Roll No: 2310040027</h3>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

# 👤 Student Info in Sidebar (Compact Version)
with st.sidebar:
    st.image("https://img.icons8.com/bubbles/100/000000/user.png", width=100)
    st.markdown(f"""
    <div style="font-size: 0.85rem; line-height: 1.2; padding-top: 10px;">
    <strong>Name:</strong> Rizwan<br>
    <strong>Roll No:</strong> 2310040027<br>
    <strong>Course:</strong> Optimization
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# 🛠️ Dashboard Navigation Cards (Wrapped in Animation Classes)
st.markdown('<p class="explore-heading">Explore Modules</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card-1">', unsafe_allow_html=True)
    with st.container():
        st.markdown("#### 📈 Calculus & Benchmarking")
        st.write("Find critical points in 1D/2D and test unconstrained solvers on complex landscapes.")
        st.page_link("pages/01_1d_critical.py", label="1D Critical Points", icon="🔍")
        st.page_link("pages/02_2d_critical.py", label="2D Critical Points", icon="🏔️")
        st.page_link("pages/04_unconstrained.py", label="Gradient Solvers (SD/NM/CG)", icon="📉")
        st.page_link("pages/05_benchmarking.py", label="Rosenbrock & Ackley Benchmark", icon="📊")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card-2">', unsafe_allow_html=True)
    with st.container():
        st.markdown("#### 🧬 Metaheuristics & Pareto")
        st.write("Solve combinatorial and multi-objective problems using evolutionary and annealing strategies.")
        st.page_link("pages/03_pareto.py", label="Multi-Objective Pareto Front", icon="⚖️")
        st.page_link("pages/06_genetic_algo.py", label="Genetic Algorithms (Knapsack)", icon="🧬")
        st.page_link("pages/07_simulated_annealing.py", label="Simulated Annealing (Timetable)", icon="🔥")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; opacity:0.5; font-size:0.8rem; padding: 8px 0;">
    Built with ❤️ by Rizwan — 2026
</div>
""", unsafe_allow_html=True)
