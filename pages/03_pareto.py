import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import io
import os

st.title("⚖️ Multi-Objective Optimization — Pareto Front")
st.markdown("Use the built-in datasets (Laptops/Smartphones) or upload your own CSV to find the **Pareto Optimal** solutions.")

# ── Pareto logic ──────────────────────────────────────────────────────────────
def find_pareto(costs):
    """
    costs: 2D array where each column is an objective to MINIMIZE.
    Returns boolean mask — True = Pareto optimal.
    """
    n = costs.shape[0]
    is_efficient = np.ones(n, dtype=bool)
    for i in range(n):
        if not is_efficient[i]:
            continue
        dominated = np.all(costs <= costs[i], axis=1) & np.any(costs < costs[i], axis=1)
        dominated[i] = False
        is_efficient[dominated] = False
    return is_efficient

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Data Source")
    use_default = st.radio("Dataset", ["Built-in Laptops", "Built-in Smartphones", "Upload CSV"])
    uploaded = None
    if use_default == "Upload CSV":
        uploaded = st.file_uploader("Upload CSV", type=["csv"])

    st.markdown("---")
    st.header("Objectives")
    st.caption("Select two columns and their optimization direction.")

# ── Load data ─────────────────────────────────────────────────────────────────
data_path = "data/"
if use_default == "Upload CSV" and uploaded is not None:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded {len(df)} rows from uploaded file.")
elif use_default == "Built-in Laptops":
    if os.path.exists(os.path.join(data_path, "Laptop_Model.csv")):
        df = pd.read_csv(os.path.join(data_path, "Laptop_Model.csv"))
    else:
        st.error("Laptop dataset not found in data/ directory.")
        st.stop()
else:
    if os.path.exists(os.path.join(data_path, "Smartphone_Model.csv")):
        df = pd.read_csv(os.path.join(data_path, "Smartphone_Model.csv"))
    else:
        st.error("Smartphone dataset not found in data/ directory.")
        st.stop()

st.subheader("Dataset Preview")
st.dataframe(df, use_container_width=True)

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

if len(numeric_cols) < 2:
    st.error("Need at least 2 numeric columns for multi-objective optimization.")
    st.stop()

with st.sidebar:
    obj1_col = st.selectbox("Objective 1 (X axis)", numeric_cols, index=0)
    obj1_dir = st.radio("Direction 1", ["Minimize", "Maximize"], index=0, horizontal=True)
    obj2_col = st.selectbox("Objective 2 (Y axis)", numeric_cols,
                             index=1 if len(numeric_cols) > 1 else 0)
    obj2_dir = st.radio("Direction 2", ["Minimize", "Maximize"], index=0, horizontal=True)
    
    label_candidates = ["(none)"] + df.select_dtypes(exclude=np.number).columns.tolist()
    label_col = st.selectbox("Label column (optional)", label_candidates)
    
    run_btn = st.button("Calculate Pareto Front", type="primary", use_container_width=True)

st.markdown("---")

# ── Run Algorithm ─────────────────────────────────────────────────────────────
if run_btn:
    v1 = df[obj1_col].values.astype(float)
    v2 = df[obj2_col].values.astype(float)

    # Flip values to minimize if user chose 'Maximize'
    c1 = v1 if obj1_dir == "Minimize" else -v1
    c2 = v2 if obj2_dir == "Minimize" else -v2
    costs = np.column_stack([c1, c2])

    mask = find_pareto(costs)
    df["Pareto"] = mask
    pareto_df   = df[mask].copy()
    dominated_df = df[~mask].copy()

    # ── Summary Metrics ───────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("Total items", len(df))
    col2.metric("Pareto Efficient", int(mask.sum()))
    col3.metric("Dominated", int((~mask).sum()))

    # ── Visualization ───────────────────────────────────────────────────────────
    st.subheader("Visualizing Trade-offs")
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot dominated points
    ax.scatter(dominated_df[obj1_col], dominated_df[obj2_col],
               c="lightgrey", edgecolors="grey", s=60, alpha=0.5, label="Dominated", zorder=2)
    
    # Plot Pareto points
    ax.scatter(pareto_df[obj1_col], pareto_df[obj2_col],
               c="crimson", edgecolors="black", s=100, label="Pareto Front", zorder=3)

    # Draw the front line
    # Depending on directions, the front line looks different.
    # Simple staircase for sorted points
    pf_sorted = pareto_df.sort_values(by=obj1_col)
    ax.step(pf_sorted[obj1_col], pf_sorted[obj2_col], where='post', color="red", alpha=0.4, linestyle="--", zorder=2)

    # Annotate points if requested
    if label_col != "(none)":
        for _, row in pareto_df.iterrows():
            ax.annotate(str(row[label_col]),
                        (row[obj1_col], row[obj2_col]),
                        xytext=(5, 5), textcoords="offset points",
                        fontsize=9, color="darkred")

    ax.set_xlabel(f"{obj1_col} ({obj1_dir})", fontsize=11)
    ax.set_ylabel(f"{obj2_col} ({obj2_dir})", fontsize=11)
    ax.set_title("Pareto Front Boundary", fontsize=13)
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.5)
    st.pyplot(fig)

    # ── Detailed Pareto Results ──────────────────────────────────────────────────────────
    st.subheader("Optimal Candidates Table")
    display_cols = ([label_col] if label_col != "(none)" else []) + [obj1_col, obj2_col]
    st.dataframe(pareto_df[display_cols].reset_index(drop=True), use_container_width=True)

    # ── Export ──────────────────────────────────────────────────────────────
    csv_buf = io.StringIO()
    pareto_df.to_csv(csv_buf, index=False)
    st.download_button("📥 Download Pareto Solutions (CSV)",
                       data=csv_buf.getvalue(),
                       file_name="pareto_optimization_results.csv",
                       mime="text/csv",
                       use_container_width=True)
else:
    st.info("Choose objectives in the sidebar and click **Calculate Pareto Front**.")
    st.markdown("""
    **Understanding the Pareto Front:**
    - A point is **Pareto optimal** if you cannot improve one objective (e.g., lower price) without worsening another (e.g., lower performance).
    - The points in red represent the *best trade-offs* available in your dataset.
    """)
