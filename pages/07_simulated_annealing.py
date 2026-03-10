import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

st.title("🔥 Simulated Annealing")
st.markdown("Solve the **Exam Timetable Scheduling Problem** to minimize scheduling clashes for students. Adjust the cooling parameters to control the algorithm's exploration.")

# ---------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------
st.sidebar.header("SA Parameters")

num_slots = st.sidebar.slider("Number of time slots", 3, 8, 5)
initial_temp = st.sidebar.number_input("Initial Temperature", value=100.0)
cooling_rate = st.sidebar.slider("Cooling rate", 0.50, 0.999, 0.995, 0.001)
min_temp = st.sidebar.number_input("Min Temperature", value=0.1)
max_iterations = st.sidebar.slider("Max Iterations", 100, 10000, 5000, 100)
random_seed = st.sidebar.number_input("Random seed", value=42)

# =============================================================================
# PROBLEM DATA
# =============================================================================
EXAMS = [
    "Mathematics", "Physics", "Chemistry", "English", "History",
    "Computer Science", "Economics", "Biology", "Statistics", "Geography"
]
NUM_EXAMS = len(EXAMS)

STUDENTS = [
    [0,1,5],[0,2,6],[1,3,7],[2,4,8],[3,5,9],
    [0,4,7],[1,6,8],[2,5,9],[3,6,0],[4,7,1],
    [5,8,2],[6,9,3],[7,0,4],[8,1,5],[9,2,6],
    [0,3,8],[1,4,9],[2,7,5],[3,8,6],[4,9,7],
    [0,5,2],[1,6,3],[2,7,4],[3,8,0],[4,9,1],
    [5,0,6],[6,1,7],[7,2,8],[8,3,9],[9,4,0],
]

with st.expander("Show Problem Details"):
    st.write(f"**Total Exams**: {NUM_EXAMS}")
    st.write(f"**Available Time Slots**: {num_slots}")
    st.write(f"**Total Students**: {len(STUDENTS)} (each taking 3 exams)")

# =============================================================================
# ALGORITHM DEFINITIONS
# =============================================================================
def count_clashes(timetable):
    clashes = 0
    for student_exams in STUDENTS:
        seen_slots = set()
        for exam in student_exams:
            slot = timetable[exam]
            if slot in seen_slots:
                clashes += 1
            seen_slots.add(slot)
    return clashes

def generate_neighbor(timetable):
    new_tt = timetable[:]
    exam = random.randint(0, NUM_EXAMS - 1)
    current_slot = timetable[exam]
    new_slot = random.choice([s for s in range(num_slots) if s != current_slot])
    new_tt[exam] = new_slot
    return new_tt

def run_sa():
    random.seed(random_seed)

    current   = [random.randint(0, num_slots - 1) for _ in range(NUM_EXAMS)]
    current_c = count_clashes(current)
    best      = current[:]
    best_c    = current_c

    T         = initial_temp
    clash_log, temp_log, accept_log = [], [], []
    accepts = 0

    for it in range(max_iterations):
        if T < min_temp:
            break

        neighbour   = generate_neighbor(current)
        neighbour_c = count_clashes(neighbour)
        delta       = neighbour_c - current_c

        accepted = False
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            current   = neighbour
            current_c = neighbour_c
            accepted  = True
            accepts  += 1

        if current_c < best_c:
            best   = current[:]
            best_c = current_c

        clash_log.append(best_c)
        temp_log.append(T)
        accept_log.append(accepts / (it + 1))
        T *= cooling_rate

        if best_c == 0:
            break

    return best, best_c, clash_log, temp_log, accept_log

# =============================================================================
# EXECUTION & RESULTS
# =============================================================================
if st.sidebar.button("Run Simulated Annealing", type="primary", use_container_width=True):
    with st.spinner("Heating and cooling..."):
        tt, clashes, clash_log, temp_log, accept_log = run_sa()
        
    st.subheader("Performance Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Final Clashes", clashes)
    col2.metric("Starting Clashes", clash_log[0])
    col3.metric("Iterations", len(clash_log))
    col4.metric("Status", "✅ Solved" if clashes == 0 else "⚠️ Partial")
    
    # Graphs
    st.subheader("Optimization Analysis")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].plot(clash_log, color="crimson", linewidth=2)
    axes[0].set_title("Clashes over Time")
    axes[0].set_xlabel("Iteration")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(temp_log, color="steelblue", linewidth=2)
    axes[1].set_title("Temperature Schedule")
    axes[1].set_xlabel("Iteration")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(accept_log, color="darkorange", linewidth=2)
    axes[2].set_title("Acceptance Rate")
    axes[2].set_xlabel("Iteration")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
        
    c_left, c_right = st.columns([1, 1])
    
    with c_left:
        st.subheader("Final Timetable")
        timetable_data = []
        for slot in range(num_slots):
            in_slot = [EXAMS[i] for i in range(NUM_EXAMS) if tt[i] == slot]
            timetable_data.append({"Slot": f"Slot {slot+1}", "Exams": ", ".join(in_slot) if in_slot else "(empty)"})
        st.dataframe(pd.DataFrame(timetable_data), use_container_width=True, hide_index=True)
    
    with c_right:
        st.subheader("Assignment Heatmap")
        fig_heat, ax_heat = plt.subplots(figsize=(6, 5))
        grid = np.zeros((num_slots, NUM_EXAMS))
        for exam_i, slot in enumerate(tt):
            grid[slot, exam_i] = 1
        im = ax_heat.imshow(grid, cmap="YlOrRd", aspect="auto")
        ax_heat.set_xticks(range(NUM_EXAMS))
        ax_heat.set_xticklabels([e[:4] for e in EXAMS], rotation=45)
        ax_heat.set_yticks(range(num_slots))
        ax_heat.set_yticklabels([f"S{s+1}" for s in range(num_slots)])
        plt.colorbar(im, ax=ax_heat, shrink=0.6)
        st.pyplot(fig_heat)

    with st.expander("Show Student Conflict Details"):
        clash_rows = []
        for si, student_exams in enumerate(STUDENTS):
            seen = {}
            for e in student_exams:
                s = tt[e]
                seen[s] = seen.get(s, 0) + 1
            student_clashes = sum(v - 1 for v in seen.values() if v > 1)
            clash_rows.append({
                "Student": si+1,
                "Exams": ", ".join(EXAMS[e] for e in student_exams),
                "Slots": ", ".join(str(tt[e]+1) for e in student_exams),
                "Clashes": student_clashes
            })
        st.dataframe(pd.DataFrame(clash_rows), use_container_width=True, hide_index=True)

else:
    st.info("Configure SA parameters in the sidebar and click 'Run Simulated Annealing'.")
    st.markdown("""
    **Recommended Cooling Schedules:**
    | Strategy | Cooling Rate | Behavior |
    |---|---|---|
    | **Fast** | 0.80 | Quick convergence, high chance of local minima |
    | **Balanced** | 0.95 | Solid trade-off |
    | **Slow** | 0.995 | Deep search, high accuracy (default) |
    """)
