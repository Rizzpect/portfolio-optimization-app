import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import pandas as pd

st.title("🔥 Simulated Annealing")
st.markdown("Solve the **Exam Timetable Scheduling Problem** to minimize scheduling clashes for students. Adjust the cooling parameters to control the algorithm's exploration.")

# ---------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------
st.sidebar.header("SA Parameters")

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
NUM_SLOTS = 5

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
    st.write(f"**Available Time Slots**: {NUM_SLOTS}")
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
    new_slot = random.choice([s for s in range(NUM_SLOTS) if s != current_slot])
    new_tt[exam] = new_slot
    return new_tt

def run_sa():
    random.seed(random_seed)

    current   = [random.randint(0, NUM_SLOTS - 1) for _ in range(NUM_EXAMS)]
    current_c = count_clashes(current)
    best      = current[:]
    best_c    = current_c

    T         = initial_temp
    clash_log = []
    temp_log  = []

    for _ in range(max_iterations):
        if T < min_temp:
            break

        neighbour   = generate_neighbor(current)
        neighbour_c = count_clashes(neighbour)
        delta       = neighbour_c - current_c

        # Always accept improvements; sometimes accept worse solutions
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            current   = neighbour
            current_c = neighbour_c

        if current_c < best_c:
            best   = current[:]
            best_c = current_c

        clash_log.append(best_c)
        temp_log.append(T)
        T *= cooling_rate

        if best_c == 0:
            break

    return best, best_c, clash_log, temp_log

# =============================================================================
# EXECUTION & RESULTS
# =============================================================================
if st.sidebar.button("Run Algorithm"):
    with st.spinner("Running Simulated Annealing..."):
        tt, clashes, clash_log, temp_log = run_sa()
        
    st.subheader("Results")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Iterations Run", len(clash_log))
    col2.metric("Starting Clashes", clash_log[0] if clash_log else "N/A")
    col3.metric("Final Clashes", clashes)
    
    if clashes == 0:
        st.success("Perfect timetable! No student clashes.")
    elif clashes < clash_log[0]:
        st.warning("Found a better timetable, but still has clashes. Try adjusting parameters.")
    else:
        st.error("Could not find a better timetable.")
        
    st.markdown("### Final Timetable")
    
    timetable_data = []
    for slot in range(NUM_SLOTS):
        in_slot = [EXAMS[i] for i in range(NUM_EXAMS) if tt[i] == slot]
        timetable_data.append({"Slot": f"Slot {slot+1}", "Exams": ", ".join(in_slot) if in_slot else "(empty)"})
        
    st.dataframe(pd.DataFrame(timetable_data), use_container_width=True)
    
    st.markdown("### SA Convergence")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(clash_log, color="crimson", linewidth=1.5)
    ax1.set_ylabel("Minimal Clashes Found")
    ax1.set_title(f"SA Convergence (Cooling={cooling_rate}, Temp={initial_temp})")
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(temp_log, color="steelblue", linewidth=1.5)
    ax2.set_ylabel("Temperature")
    ax2.set_xlabel("Iteration")
    ax2.grid(True, alpha=0.3)
    
    st.pyplot(fig)
else:
    st.info("Configure SA parameters in the sidebar and click 'Run Algorithm'.")
