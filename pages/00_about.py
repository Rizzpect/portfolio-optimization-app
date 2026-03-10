import streamlit as st

st.title("🚀 Optimization Portfolio")
st.markdown("""
Welcome to my optimization portfolio! This application aggregates all the projects and assignments completed for the Optimization course. 
I have integrated interactive visualizations and solvers for various calculus and metaheuristic problems.

**Name:** Rizwan  
**Roll No:** 2310040027
""")

st.markdown("---")

# 👤 Student Info
with st.sidebar:
    st.image("https://img.icons8.com/bubbles/100/000000/user.png", width=100)
    st.header("Student Info")
    st.write("**Name:** Rizwan")
    st.write("**Roll No:** 2310040027")
    st.write("**Course:** Optimization in Engineering")

# 🛠️ Dashboard Navigation Cards (Inspired by Prof's layout)
st.subheader("Explore Modules")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### 📈 Calculus & Benchmarking")
        st.write("Find critical points in 1D/2D and test unconstrained solvers on complex landscapes.")
        st.page_link("pages/01_1d_critical.py", label="1D Critical Points", icon="🔍")
        st.page_link("pages/02_2d_critical.py", label="2D Critical Points", icon="🏔️")
        st.page_link("pages/04_unconstrained.py", label="Gradient Solvers (SD/NM/CG)", icon="📉")
        st.page_link("pages/05_benchmarking.py", label="Rosenbrock & Ackley Benchmark", icon="📊")

with col2:
    with st.container(border=True):
        st.markdown("#### 🧬 Metaheuristics & Pareto")
        st.write("Solve combinatorial and multi-objective problems using evolutionary and annealing strategies.")
        st.page_link("pages/03_pareto.py", label="Multi-Objective Pareto Front", icon="⚖️")
        st.page_link("pages/06_genetic_algo.py", label="Genetic Algorithms (Knapsack)", icon="🧬")
        st.page_link("pages/07_simulated_annealing.py", label="Simulated Annealing (Timetable)", icon="🔥")

st.markdown("---")
st.caption("Developed by Rizwan - 2026")
