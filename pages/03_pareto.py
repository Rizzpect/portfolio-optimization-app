import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

st.title("⚖️ Pareto Front Optimization")
st.markdown("Identify non-dominated (Pareto optimal) solutions from a given dataset based on conflicting multi-objective metrics.")

st.sidebar.header("Dataset Selection")
dataset_option = st.sidebar.radio(
    "Choose a dataset:",
    ("Laptops", "Smartphones")
)

# Load dataset
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
if dataset_option == "Laptops":
    file_path = os.path.join(data_dir, "Laptop_Model.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        st.error(f"Dataset not found at {file_path}")
        df = pd.DataFrame()
else:
    file_path = os.path.join(data_dir, "Smartphone_Model.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        st.error(f"Dataset not found at {file_path}")
        df = pd.DataFrame()

if not df.empty:
    st.subheader(f"{dataset_option} Dataset")
    st.dataframe(df.head(10), use_container_width=True)
    
    # Let user select objectives
    st.sidebar.subheader("Objective Configuration")
    all_numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    # Auto-detect sensible defaults based on dataset
    default_min = []
    default_max = []
    if dataset_option == "Laptops":
        default_min = ["Price ($)", "Weight (kg)"] if "Price ($)" in all_numeric_cols else []
        default_max = ["Performance Score (out of 100)", "Battery Life (hours)"] if "Performance Score (out of 100)" in all_numeric_cols else []
    else:
        default_min = ["Price ($)", "Weight (grams)"] if "Price ($)" in all_numeric_cols else []
        default_max = ["Performance Score (out of 100)", "Battery Life (hours)"] if "Performance Score (out of 100)" in all_numeric_cols else []
        
    # Filter valid columns
    default_min = [c for c in default_min if c in all_numeric_cols]
    default_max = [c for c in default_max if c in all_numeric_cols]
        
    minimize_cols = st.sidebar.multiselect("Objectives to Minimize:", all_numeric_cols, default=default_min)
    maximize_cols = st.sidebar.multiselect("Objectives to Maximize:", all_numeric_cols, default=default_max)
    
    if st.sidebar.button("Calculate Pareto Front"):
        if not minimize_cols and not maximize_cols:
            st.warning("Please select at least one objective.")
        elif len(minimize_cols) + len(maximize_cols) < 2:
            st.warning("Please select at least two objectives to find trade-offs.")
        else:
            with st.spinner("Finding Pareto optimal solutions..."):
                def is_dominated(row1, row2, min_cols, max_cols):
                    """Returns True if row1 is dominated by row2."""
                    dominated_min = all(row2[col] <= row1[col] for col in min_cols) and any(row2[col] < row1[col] for col in min_cols)
                    dominated_max = all(row2[col] >= row1[col] for col in max_cols) and any(row2[col] > row1[col] for col in max_cols)
                    
                    if not min_cols: return dominated_max
                    if not max_cols: return dominated_min
                    
                    # Both min and max conditions must hold or be equal, and at least one must be strictly better
                    all_as_good_or_better = all(row2[col] <= row1[col] for col in min_cols) and all(row2[col] >= row1[col] for col in max_cols)
                    strictly_better = any(row2[col] < row1[col] for col in min_cols) or any(row2[col] > row1[col] for col in max_cols)
                    
                    return all_as_good_or_better and strictly_better
                
                n = len(df)
                is_pareto = np.ones(n, dtype=bool)
                
                for i in range(n):
                    if not is_pareto[i]: continue
                    for j in range(n):
                        if i == j or not is_pareto[j]: continue
                        if is_dominated(df.iloc[i], df.iloc[j], minimize_cols, maximize_cols):
                            is_pareto[i] = False
                            break
                            
                pareto_df = df[is_pareto].copy()
            
            st.success(f"Found {len(pareto_df)} Pareto optimal solutions out of {n} total.")
            
            st.subheader("🏆 Pareto Optimal Set")
            st.dataframe(pareto_df, use_container_width=True)
            
            # Visualization (2D scatter if exactly 2 objectives are selected, otherwise pick first two)
            selected_objs = minimize_cols + maximize_cols
            if len(selected_objs) >= 2:
                obj_x = selected_objs[0]
                obj_y = selected_objs[1]
                
                st.subheader(f"Visualization: {obj_x} vs {obj_y}")
                
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Plot dominated points
                dominated_df = df[~is_pareto]
                ax.scatter(dominated_df[obj_x], dominated_df[obj_y], color='gray', alpha=0.5, label='Dominated')
                
                # Plot Pareto points
                ax.scatter(pareto_df[obj_x], pareto_df[obj_y], color='red', s=60, label='Pareto Optimal')
                
                # Annotate Pareto points (if text column exists)
                model_col_candidates = [col for col in df.columns if 'Model' in str(col) or df[col].dtype == object]
                if model_col_candidates:
                    model_col = model_col_candidates[0]
                    for idx, row in pareto_df.iterrows():
                        ax.annotate(row[model_col], (row[obj_x], row[obj_y]), 
                                  xytext=(5, 5), textcoords='offset points', 
                                  fontsize=8, alpha=0.8)
                
                ax.set_xlabel(obj_x)
                ax.set_ylabel(obj_y)
                ax.set_title(f"Pareto Front ({obj_x} vs {obj_y})")
                
                # Direction of goodness
                # Add arrows indicating direction
                x_dir = -1 if obj_x in minimize_cols else 1
                y_dir = -1 if obj_y in minimize_cols else 1
                
                # Adjust axes to show the ideal direction
                ax.legend()
                ax.grid(True, alpha=0.3)
                
                st.pyplot(fig)
            else:
                st.info("Select at least 2 numeric objectives to see a scatter plot visualization.")
