import streamlit as st

st.set_page_config(
    page_title="Optimization Portfolio | Rizwan",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
