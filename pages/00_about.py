import streamlit as st
import time

# --- EXTREME UI EXTRAS: GOOGLE FONTS & ADVANCED CSS ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap" rel="stylesheet">
<style>
    /* Premium Typography - Robust Fix for Icon Glitch */
    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Ensure Streamlit Icons (Material Icons) are NOT overridden */
    .material-icons, 
    .material-symbols-outlined,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarCollapse"] span,
    [data-testid="stSidebarCollapse"] i,
    [data-testid="stSidebarCollapse"] svg,
    [class*="st-emotion-cache"] i,
    [class*="st-emotion-cache"] svg,
    [class^="st-"] i {
        font-family: 'Material Icons' !important;
        font-feature-settings: 'liga' !important;
    }

    /* SIDEBAR LOCK: Hide toggle buttons and header for a cleaner look */
    [data-testid="stSidebarCollapse"], 
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Ensure Sidebar stays visible but maintains its default width */
    [data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 280px !important;
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
        animation: float 4s ease-in-out infinite;
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

st.markdown("---")

# 👤 Student Info in Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/bubbles/100/000000/user.png", width=120)
    st.header("Student Info")
    st.info(f"**Name:** Rizwan\n\n**Roll No:** 2310040027\n\n**Course:** Optimization in Engineering")

# 🛠️ Dashboard Navigation Cards (Wrapped in Animation Classes)
st.subheader("Explore Modules")

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

st.markdown("---")
st.caption("Developed by Rizwan - 2026")
