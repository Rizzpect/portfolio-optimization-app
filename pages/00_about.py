import streamlit as st

# --- CUSTOM CSS FOR ANIMATIONS & MODERN UI ---
st.markdown("""
<style>
    /* Global Page Fade-in */
    .main .block-container {
        animation: fadeIn 0.8s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Glassmorphism Card Style */
    .stColumn > div > div > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease-in-out;
    }

    /* Hover Lift & Glow Effect */
    .stColumn > div > div > div:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        background: rgba(255, 255, 255, 0.08);
    }

    /* Gradient Title */
    .gradient-text {
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        font-size: 3rem;
    }

    /* Floating Profile Pic Animation */
    [data-testid="stSidebar"] img {
        border-radius: 50%;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="gradient-text">🚀 Optimization Portfolio</h1>', unsafe_allow_html=True)

st.markdown("""
Welcome to my optimization portfolio! This application aggregates all the projects and assignments completed for the Optimization course. 
I have integrated interactive visualizations and solvers for various calculus and metaheuristic problems.

**Name:** Rizwan  
**Roll No:** 2310040027
""")

st.markdown("---")

# 👤 Student Info in Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/bubbles/100/000000/user.png", width=120)
    st.header("Student Info")
    st.write("**Name:** Rizwan")
    st.write("**Roll No:** 2310040027")
    st.write("**Course:** Optimization in Engineering")

# 🛠️ Dashboard Navigation Cards
st.subheader("Explore Modules")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.markdown("#### 📈 Calculus & Benchmarking")
        st.write("Find critical points in 1D/2D and test unconstrained solvers on complex landscapes.")
        st.page_link("pages/01_1d_critical.py", label="1D Critical Points", icon="🔍")
        st.page_link("pages/02_2d_critical.py", label="2D Critical Points", icon="🏔️")
        st.page_link("pages/04_unconstrained.py", label="Gradient Solvers (SD/NM/CG)", icon="📉")
        st.page_link("pages/05_benchmarking.py", label="Rosenbrock & Ackley Benchmark", icon="📊")

with col2:
    with st.container():
        st.markdown("#### 🧬 Metaheuristics & Pareto")
        st.write("Solve combinatorial and multi-objective problems using evolutionary and annealing strategies.")
        st.page_link("pages/03_pareto.py", label="Multi-Objective Pareto Front", icon="⚖️")
        st.page_link("pages/06_genetic_algo.py", label="Genetic Algorithms (Knapsack)", icon="🧬")
        st.page_link("pages/07_simulated_annealing.py", label="Simulated Annealing (Timetable)", icon="🔥")

st.markdown("---")
st.caption("Developed by Rizwan - 2026 | Modern UI/UX Enhanced")
