import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd

st.title("🧬 Genetic Algorithms")
st.markdown("Solve the **0/1 Knapsack Problem** using a Genetic Algorithm. Adjust the parameters to see how exploration vs exploitation affects the solution.")

# ---------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------
st.sidebar.header("GA Parameters")

max_weight = st.sidebar.slider("Max weight (kg)", 5.0, 30.0, 15.0, 0.5)
population_size = st.sidebar.slider("Population size", 10, 100, 20, 1)
generations = st.sidebar.slider("Generations", 10, 200, 50, 1)
mutation_rate = st.sidebar.slider("Mutation rate", 0.01, 0.50, 0.05, 0.01)
crossover_rate = st.sidebar.slider("Crossover rate", 0.50, 1.00, 0.80, 0.01)
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
    result = chromosome[:]
    for i in range(NUM_ITEMS):
        if random.random() < rate:
            result[i] = 1 - result[i]
    return result

def run_ga():
    random.seed(random_seed)

    population = [
        [random.randint(0, 1) for _ in range(NUM_ITEMS)]
        for _ in range(population_size)
    ]

    best_chromosome = None
    best_value      = -1
    value_log       = []

    for _ in range(generations):
        fitnesses = [fitness(c) for c in population]

        gen_best_i = max(range(population_size), key=lambda i: fitnesses[i])
        if fitnesses[gen_best_i] > best_value:
            best_value      = fitnesses[gen_best_i]
            best_chromosome = population[gen_best_i][:]

        value_log.append(best_value)

        # Elitism
        next_gen = [best_chromosome[:]]
        while len(next_gen) < population_size:
            p1    = tournament_select(population, fitnesses, tournament_size)
            p2    = tournament_select(population, fitnesses, tournament_size)
            child = crossover(p1, p2, crossover_rate)
            child = mutate(child, mutation_rate)
            next_gen.append(child)

        population = next_gen

    return best_chromosome, best_value, value_log

# =============================================================================
# EXECUTION & RESULTS
# =============================================================================
if st.sidebar.button("Run Algorithm"):
    with st.spinner("Running Genetic Algorithm..."):
        best_chr, best_val, val_log = run_ga()
        
    st.subheader("Results")
    
    total_weight = sum(WEIGHTS[i] for i in range(NUM_ITEMS) if best_chr[i] == 1)
    packed_items = [NAMES[i] for i in range(NUM_ITEMS) if best_chr[i] == 1]
    valid = total_weight <= max_weight
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Value", best_val)
    col2.metric("Total Weight", f"{total_weight:.1f} kg")
    col3.metric("Capacity", f"{max_weight:.1f} kg")
    
    if not valid:
        st.error(f"Invalid solution! Weight exceeded maximum capacity.")
    else:
        st.success("Valid packing configuration found!")
        
    st.markdown("### Packed Items")
    df_packed = pd.DataFrame({
        "Item": packed_items,
        "Weight": [WEIGHTS[NAMES.index(i)] for i in packed_items],
        "Value": [VALUES[NAMES.index(i)] for i in packed_items]
    })
    st.dataframe(df_packed, use_container_width=True)
    
    st.markdown("### GA Convergence")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(val_log, color="seagreen", linewidth=2, marker="o", markersize=3)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Value")
    ax.set_title(f"GA Convergence (Mutation={mutation_rate}, Pop={population_size})")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
else:
    st.info("Configure GA parameters in the sidebar and click 'Run Algorithm'.")
