import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 Critical Points in 1D")
st.markdown("Find and classify critical points of a single-variable function $f(x)$ using the First and Second Derivative Tests.")

# Input Section
st.sidebar.header("Function Input")
expr_string = st.sidebar.text_input("Enter f(x):", value="x**4 - 8*x**2 + 10")
x_min = st.sidebar.number_input("Plot X Min", value=-4.0)
x_max = st.sidebar.number_input("Plot X Max", value=4.0)

try:
    x = sp.Symbol('x')
    f = sp.sympify(expr_string)
    
    st.markdown(f"**Function:** $\\quad f(x) = {sp.latex(f)}$")
    
    f_prime = sp.diff(f, x)
    f_double_prime = sp.diff(f_prime, x)
    
    st.markdown(f"**First Derivative:** $\\quad f'(x) = {sp.latex(f_prime)}$")
    st.markdown(f"**Second Derivative:** $\\quad f''(x) = {sp.latex(f_double_prime)}$")
    
    # Computation
    with st.spinner("Calculating critical points..."):
        critical_points = sp.solve(f_prime, x)
        real_critical_points = [pt.evalf() for pt in critical_points if pt.is_real]
    
    if not real_critical_points:
        st.warning("No real critical points found.")
    else:
        st.subheader("Critical Points Analysis")
        results = []
        
        for pt in real_critical_points:
            f_val = f.subs(x, pt).evalf()
            second_deriv_val = f_double_prime.subs(x, pt).evalf()
            
            if second_deriv_val > 0:
                classification = "Local Minimum"
            elif second_deriv_val < 0:
                classification = "Local Maximum"
            else:
                classification = "Saddle Point / Inconclusive"
                
            results.append({
                "x": float(pt),
                "f(x)": float(f_val),
                "f''(x)": float(second_deriv_val),
                "Classification": classification
            })
            
        st.dataframe(results, use_container_width=True)
        
        # Plotting
        st.subheader("Function Visualization")
        
        # Convert sympy expression to a fast numerical function
        f_num = sp.lambdify(x, f, "numpy")
        
        x_vals = np.linspace(x_min, x_max, 400)
        y_vals = f_num(x_vals)
        
        # Handle cases where user inputs a constant function (which returns a scalar)
        if np.isscalar(y_vals):
            y_vals = np.full_like(x_vals, y_vals)
            
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x_vals, y_vals, label=f"f(x) = {expr_string}", color="#2E86AB")
        
        # Plot critical points
        for res in results:
            cx, cy = res["x"], res["f(x)"]
            classification = res["Classification"]
            
            color = "green" if "Minimum" in classification else "red" if "Maximum" in classification else "orange"
            ax.scatter([cx], [cy], color=color, s=100, zorder=5, label=f"{classification} at x={cx:.2f}")
            
        ax.set_title("Function Plot with Critical Points")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True, alpha=0.3)
        ax.autoscale()
        
        # Avoid duplicate labels in legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())
        
        st.pyplot(fig)

except Exception as e:
    st.error(f"Error parsing or evaluating the function: {e}")
