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
    html, body, [class*="st-"]:not(.material-icons):not(.material-symbols-outlined):not(i):not(svg) {
        font-family: 'Outfit', sans-serif !important;
    }

    /* CRITICAL FIX: Ensure Streamlit Icons (Material Icons) render correctly */
    .material-icons, 
    .material-symbols-outlined {
        font-family: 'Material Symbols Outlined', 'Material Icons' !important;
        font-feature-settings: 'liga' !important;
    }

    /* SIDEBAR LOCK: Hide toggle buttons and header for a cleaner look */
    [data-testid="stSidebarCollapse"], 
    [data-testid="collapsedControl"],
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebar"] > div:first-child > button,
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    /* Hide any raw icon text that leaks when Material Icons fail */
    [data-testid="stSidebar"] span.material-symbols-outlined,
    [data-testid="stSidebar"] span[class*="icon"] {
        font-size: 0 !important;
        visibility: hidden !important;
    }
    [data-testid="stSidebarNavItems"] ul {
        padding-top: 0rem !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Ensure Sidebar stays visible and CANNOT be collapsed */
    [data-testid="stSidebar"] {
        min-width: 280px !important;
        max-width: 280px !important;
        width: 280px !important;
        transform: none !important;
        transition: none !important;
        visibility: visible !important;
        display: flex !important;
        position: relative !important;
    }
    /* Override Streamlit's collapsed state — force sidebar open */
    [data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 280px !important;
        max-width: 280px !important;
        width: 280px !important;
        transform: none !important;
        margin-left: 0 !important;
        left: 0 !important;
        display: flex !important;
        visibility: visible !important;
    }
    /* Prevent the main content from expanding full-width when sidebar collapses */
    .stAppViewBlockContainer,
    [data-testid="stAppViewBlockContainer"] {
        margin-left: 280px !important;
    }

    /* COMPACT NAV */
    [data-testid="stSidebar"] section {
        overflow-y: auto !important;
    }
    [data-testid="stSidebarNavItems"] {
        padding-top: 0px !important;
    }
    [data-testid="stSidebarNavItems"] li {
        margin-bottom: 0px !important;
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

    /* ── Sidebar Nav Link Hover Glow ── */
    [data-testid="stSidebarNavItems"] a {
        transition: all 0.25s ease !important;
        border-radius: 8px !important;
    }
    [data-testid="stSidebarNavItems"] a:hover {
        background: rgba(0, 201, 255, 0.08) !important;
        padding-left: 12px !important;
        box-shadow: inset 3px 0 0 0 #00C9FF;
    }

    /* ── Active Page Accent Bar ── */
    [data-testid="stSidebarNavItems"] a[aria-current="page"] {
        background: rgba(0, 201, 255, 0.12) !important;
        box-shadow: inset 3px 0 0 0 #92FE9D;
    }

    /* ── Animated Gradient Border on Sidebar ── */
    [data-testid="stSidebar"] {
        border-right: 2px solid transparent !important;
        border-image: linear-gradient(180deg, #00C9FF 0%, #92FE9D 50%, #00C9FF 100%) 1 !important;
        animation: borderShift 6s linear infinite !important;
    }
    @keyframes borderShift {
        0%   { border-image: linear-gradient(180deg, #00C9FF 0%, #92FE9D 50%, #00C9FF 100%) 1; }
        33%  { border-image: linear-gradient(180deg, #92FE9D 0%, #00C9FF 50%, #92FE9D 100%) 1; }
        66%  { border-image: linear-gradient(180deg, #00C9FF 0%, #c792fe 50%, #00C9FF 100%) 1; }
        100% { border-image: linear-gradient(180deg, #00C9FF 0%, #92FE9D 50%, #00C9FF 100%) 1; }
    }

    /* ── Metric Cards Subtle Hover Lift ── */
    [data-testid="stMetric"] {
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        border-radius: 12px;
        padding: 8px;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0, 201, 255, 0.15);
    }

    /* ── DataFrame / Table Hover Row Highlight ── */
    [data-testid="stDataFrame"] {
        transition: box-shadow 0.3s ease;
        border-radius: 12px;
        overflow: hidden;
    }
    [data-testid="stDataFrame"]:hover {
        box-shadow: 0 4px 24px rgba(0, 201, 255, 0.1);
    }

    /* ── Primary Button Gradient Upgrade ── */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%) !important;
        color: #0E1117 !important;
        font-weight: 600 !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="stBaseButton-primary"]:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 20px rgba(0, 201, 255, 0.4) !important;
    }

    /* ── Expander Smooth Open ── */
    [data-testid="stExpander"] {
        transition: all 0.3s ease;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }
    [data-testid="stExpander"]:hover {
        border-color: rgba(0, 201, 255, 0.2) !important;
    }

    /* ── Styled Scrollbar ── */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 201, 255, 0.25);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 201, 255, 0.5);
    }

    /* ── Slider Track Accent ── */
    [data-testid="stSlider"] [role="slider"] {
        transition: box-shadow 0.2s ease;
    }
    [data-testid="stSlider"] [role="slider"]:hover {
        box-shadow: 0 0 8px rgba(0, 201, 255, 0.5);
    }

    /* ── Info/Warning/Error Box Polish ── */
    [data-testid="stAlert"] {
        border-radius: 10px !important;
        animation: fadeIn 0.4s ease-out;
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
