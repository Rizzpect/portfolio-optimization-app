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

    /* SIDEBAR LOCK: Hide toggle buttons and header for a cleaner look */
    [data-testid="stSidebarCollapse"], 
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    [data-testid="stSidebarNavItems"] ul {
        padding-top: 0rem !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Ensure Sidebar stays visible but maintains its default width */
    [data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 280px !important;
    }

    /* DISABLE SIDEBAR SCROLLING & COMPACT NAV */
    [data-testid="stSidebar"] section {
        overflow: hidden !important;
    }
    [data-testid="stSidebarNavItems"] {
        padding-top: 0px !important;
    }
    [data-testid="stSidebarNavItems"] li {
        margin-bottom: -5px !important; /* Compact links */
    }
    [data-testid="stSidebarNavItems"] a {
        padding-top: 4px !important;
        padding-bottom: 4px !important;
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
    [
        about_page,
        task1_page,
        task2_page,
        task3_page,
        task4_page,
        task5_page,
        task6_page,
        task7_page
    ]
)

pg.run()
