import streamlit as st

st.set_page_config(
    page_title="Optimization Portfolio | Rizwan",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Global CSS Injector for smooth transitions & Icon Fix
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap" rel="stylesheet">
<style>
    /* Global Premium Font */
    html, body, [class*="st-"] {
        font-family: 'Outfit', sans-serif !important;
    }

    /* CRITICAL FIX: Ensure Streamlit Icons (Material Icons) render correctly */
    .material-icons, 
    .material-symbols-outlined,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarCollapse"] span,
    [data-testid="stSidebarCollapse"] i,
    [class*="st-emotion-cache"] i,
    [class*="st-emotion-cache"] svg,
    [class^="st-"] i {
        font-family: 'Material Icons' !important;
        font-feature-settings: 'liga' !important;
    }

    /* Global Page Fade-in */
    .main .block-container {
        animation: fadeIn 0.6s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# Define pages for multi-page app
about_page = st.Page("pages/00_about.py", title="About Me", icon="👤", default=True)
task1_page = st.Page("pages/01_1d_critical.py", title="1D Critical Points", icon="📈")
task2_page = st.Page("pages/02_2d_critical.py", title="2D Critical Points", icon="🏔️")
task3_page = st.Page("pages/03_pareto.py", title="Pareto Front", icon="⚖️")
task4_page = st.Page("pages/04_unconstrained.py", title="Unconstrained Min", icon="📉")
task5_page = st.Page("pages/05_benchmarking.py", title="Benchmarking (Assgn 5)", icon="📊")
task6_page = st.Page("pages/06_genetic_algo.py", title="Genetic Algorithms", icon="🧬")
task7_page = st.Page("pages/07_simulated_annealing.py", title="Simulated Annealing", icon="🔥")


pg = st.navigation(
    {
        "Overview": [about_page],
        "Calculus & Optimization": [task1_page, task2_page, task4_page, task5_page],
        "Multi-Objective Optimization": [task3_page],
        "Metaheuristic Algorithms": [task6_page, task7_page],
    }
)

pg.run()
