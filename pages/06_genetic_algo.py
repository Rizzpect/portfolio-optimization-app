import streamlit as st
import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("🧬 Genetic Algorithms")
st.markdown("Solve the **0/1 Knapsack Problem** using a Genetic Algorithm. Adjust the parameters to see how exploration vs exploitation affects the solution.")

# ---------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------
st.sidebar.header("GA Parameters")

max_weight = st.sidebar.slider("Max weight (kg)", 5.0, 30.0, 15.0, 0.5)
population_size = st.sidebar.slider("Population size", 10, 100, 30, 1)
generations = st.sidebar.slider("Generations", 10, 200, 60, 1)
mutation_rate = st.sidebar.slider("Mutation rate", 0.01, 0.50, 0.05, 0.01)
crossover_rate = st.sidebar.slider("Crossover rate", 0.50, 1.00, 0.80, 0.05)
tournament_size = st.sidebar.slider("Tournament size", 2, 10, 3, 1)
random_seed = st.sidebar.number_input("Random seed", value=42)

# =============================================================================
# PROBLEM DATA
# =============================================================================
ITEMS = [
    # (name,                weight_kg,  value)
    ("Water bottle",          2.0,   9),
    ("First aid kit",         1.5,  10),
    ("Tent",                  4.0,  10),
    ("Sleeping bag",          3.0,   9),
    ("Torch",                 0.5,   6),
    ("Energy bars (x6)",      1.0,   7),
    ("Rain jacket",           1.0,   8),
    ("Map & compass",         0.3,   7),
    ("Camera",                1.2,   5),
    ("Extra clothes",         2.0,   4),
    ("Cooking stove",         1.5,   6),
    ("Rope (10 m)",           2.5,   5),
    ("Sunscreen",             0.3,   4),
    ("Trekking poles",        1.5,   5),
    ("Power bank",            0.8,   6),
]

NUM_ITEMS  = len(ITEMS)
WEIGHTS = [item[1] for item in ITEMS]
VALUES  = [item[2] for item in ITEMS]
NAMES   = [item[0] for item in ITEMS]

# Show Items Table
with st.expander("Show Available Items"):
    df_items = pd.DataFrame({
        "Item": NAMES,
        "Weight (kg)": WEIGHTS,
        "Value": VALUES
    })
    st.dataframe(df_items, use_container_width=True)

# =============================================================================
# ALGORITHM DEFINITIONS
# =============================================================================
def fitness(chromosome):
    total_weight = sum(WEIGHTS[i] for i in range(NUM_ITEMS) if chromosome[i] == 1)
    total_value  = sum(VALUES[i]  for i in range(NUM_ITEMS) if chromosome[i] == 1)
    if total_weight > max_weight:
        return 0
    return total_value

def tournament_select(population, fitnesses, k):
    candidates = random.sample(range(len(population)), k)
    winner     = max(candidates, key=lambda i: fitnesses[i])
    return population[winner][:]

def crossover(p1, p2, rate):
    if random.random() > rate:
        return p1[:]
    cut = random.randint(1, NUM_ITEMS - 1)
    return p1[:cut] + p2[cut:]

def mutate(chromosome, rate):
    return [1 - g if random.random() < rate else g for g in chromosome]

def run_ga():
    random.seed(random_seed)

    population = [
        [random.randint(0, 1) for _ in range(NUM_ITEMS)]
        for _ in range(population_size)
    ]

    best_chrom_ever = None
    best_val_ever   = -1
    
    bv_log, av_log, div_log = [], [], []

    for _ in range(generations):
        fitnesses = [fitness(c) for c in population]
        best_i = max(range(population_size), key=lambda i: fitnesses[i])
        
        if fitnesses[best_i] > best_val_ever:
            best_val_ever   = fitnesses[best_i]
            best_chrom_ever = population[best_i][:]

        bv_log.append(best_val_ever)
        valid_fits = [f for f in fitnesses if f > 0]
        av_log.append(np.mean(valid_fits) if valid_fits else 0)
        div_log.append(len(set(tuple(c) for c in population)) / population_size)

        # Elitism
        next_gen = [best_chrom_ever[:]]
        while len(next_gen) < population_size:
            p1    = tournament_select(population, fitnesses, tournament_size)
            p2    = tournament_select(population, fitnesses, tournament_size)
            child = crossover(p1, p2, crossover_rate)
            child = mutate(child, mutation_rate)
            next_gen.append(child)

        population = next_gen

    return best_chrom_ever, best_val_ever, bv_log, av_log, div_log

# =============================================================================
# EXECUTION & RESULTS
# =============================================================================
if st.sidebar.button("Run Genetic Algorithm", type="primary", use_container_width=True):
    with st.spinner("Evolving population..."):
        best_chr, best_val, bv_log, av_log, div_log = run_ga()
        
    st.subheader("Final Results")
    
    total_weight = sum(WEIGHTS[i] for i in range(NUM_ITEMS) if best_chr[i] == 1)
    packed_items = [NAMES[i] for i in range(NUM_ITEMS) if best_chr[i] == 1]
    valid = total_weight <= max_weight
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Best Value", best_val)
    col2.metric("Total Weight", f"{total_weight:.1f} kg")
    col3.metric("Status", "✅ Valid" if valid else "❌ Invalid")
    col4.metric("Items Packed", sum(best_chr))
    
    # --- Advanced Visualizations (Inspired by Prof's layout) ---
    st.subheader("GA Performance Analysis")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1: Best vs Avg
    axes[0].plot(bv_log, color="seagreen", linewidth=2, label="Best Value")
    axes[0].plot(av_log, color="steelblue", linewidth=1.5, linestyle="--", label="Avg Value")
    axes[0].set_title("Convergence Rate")
    axes[0].set_xlabel("Generation")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Improvement per Generation
    deltas = [bv_log[i] - (bv_log[i-1] if i > 0 else 0) for i in range(len(bv_log))]
    axes[1].bar(range(len(bv_log)), deltas, color="coral", alpha=0.7)
    axes[1].set_title("Value Improvement")
    axes[1].set_xlabel("Generation")
    axes[1].grid(True, alpha=0.3)

    # Plot 3: Diversity
    axes[2].plot(div_log, color="purple", linewidth=2)
    axes[2].set_title("Population Diversity")
    axes[2].set_xlabel("Generation")
    axes[2].set_ylabel("Unique/Total")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")
    
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.subheader("Best Packing Details")
        df_packed = pd.DataFrame({
            "Item": NAMES,
            "Weight": WEIGHTS,
            "Value": VALUES,
            "Packed": ["✅" if best_chr[i] else "❌" for i in range(NUM_ITEMS)]
        })
        st.dataframe(df_packed, use_container_width=True)
    
    with c_right:
        st.subheader("Composition of Value")
        packed_vals = [VALUES[i] for i in range(NUM_ITEMS) if best_chr[i] == 1]
        packed_names = [NAMES[i] for i in range(NUM_ITEMS) if best_chr[i] == 1]
        if packed_names:
            fig_bar, ax_bar = plt.subplots(figsize=(6, len(packed_names)*0.5 + 1))
            bars = ax_bar.barh(packed_names, packed_vals, color="seagreen", edgecolor="black")
            ax_bar.bar_label(bars, padding=3)
            ax_bar.set_title("Value per Packed Item")
            st.pyplot(fig_bar)

    # Chromosome Heatmap
    with st.expander("Chromosome Visualization"):
        fig_heat, ax_heat = plt.subplots(figsize=(12, 1.2))
        ax_heat.imshow([best_chr], aspect="auto", cmap="RdYlGn", vmin=0, vmax=1)
        ax_heat.set_xticks(range(NUM_ITEMS))
        ax_heat.set_xticklabels(NAMES, rotation=45, ha="right", fontsize=8)
        ax_heat.set_yticks([])
        ax_heat.set_title("Best Chromosome Structure (Green = Packed)")
        plt.tight_layout()
        st.pyplot(fig_heat)

else:
    st.info("Configure GA parameters in the sidebar and click 'Run Genetic Algorithm'.")
    st.markdown("""
    **Genetic Algorithm Process:**
    - **Selection:** Tournament selection chooses the best from a random subset.
    - **Crossover:** Single-point crossover combines parent traits.
    - **Mutation:** Random bit flips maintain genetic diversity.
    - **Elitism:** The best solution is always preserved to the next generation.
    """)
