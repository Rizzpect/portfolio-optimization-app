import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.title("📈 Critical Points in 1D")
st.markdown("Find and classify critical points of any single-variable function $f(x)$ using SymPy's symbolic differentiation.")

# ---------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------
st.sidebar.header("Function Settings")
func_str = st.sidebar.text_input("Formula f(x)", value="x**3 - 3*x + 2", help="Python/SymPy syntax (e.g., x**3 - 3*x)")
x_range = st.sidebar.slider("Plot Range", 1.0, 20.0, 5.0)

# =============================================================================
# CALCULATION & VISUALIZATION
# =============================================================================
if st.sidebar.button("Analyze Function", type="primary", use_container_width=True):
    try:
        x = sp.symbols('x')
        f_sym = sp.sympify(func_str)
        
        # Derivatives
        f_prime = sp.diff(f_sym, x)
        f_double_prime = sp.diff(f_prime, x)
        
        # Critical points
        crit_points = sp.solve(f_prime, x)
        
        st.subheader("Mathematical Derivatives")
        st.latex(f"f(x) = {sp.latex(f_sym)}")
        st.latex(f"f'(x) = {sp.latex(f_prime)}")
        st.latex(f"f''(x) = {sp.latex(f_double_prime)}")
        
        st.markdown("---")
        
        results = []
        for p in crit_points:
            try:
                p_val = complex(p).real if p.is_number else float(p.evalf())
                f_p = float(f_sym.subs(x, p_val))
                f_pp = float(f_double_prime.subs(x, p_val))
                
                classification = "Saddle/Inflection"
                if f_pp > 0: classification = "Local Minimum"
                elif f_pp < 0: classification = "Local Maximum"
                
                results.append({
                    "x": round(p_val, 4),
                    "f(x)": round(f_p, 4),
                    "f''(x)": round(f_pp, 4),
                    "Classification": classification
                })
            except Exception:
                continue
        
        if results:
            st.subheader("Critical Points Classification")
            st.dataframe(results, use_container_width=True)
            
            # Plotting
            st.subheader("Function Visualization")
            f_num = sp.lambdify(x, f_sym, 'numpy')
            x_vals = np.linspace(-x_range, x_range, 400)
            y_vals = f_num(x_vals)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(x_vals, y_vals, label=f"$f(x) = {sp.latex(f_sym)}$", color="steelblue", linewidth=2)
            
            # Mark critical points
            for res in results:
                color = "green" if "Minimum" in res["Classification"] else "red" if "Maximum" in res["Classification"] else "orange"
                ax.plot(res["x"], res["f(x)"], 'o', markersize=8, color=color, label=f"{res['Classification']} at {res['x']}")
            
            ax.axhline(0, color='black', linewidth=0.8, alpha=0.5)
            ax.axvline(0, color='black', linewidth=0.8, alpha=0.5)
            ax.grid(True, alpha=0.3)
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("No real-valued critical points found for this function.")

    except Exception as e:
        st.error(f"Error parsing function: {e}")
else:
    st.info("Enter a function in the sidebar and click **Analyze Function**.")
    st.markdown("""
    **Try these common functions:**
    - Quadratic: `x**2 - 4*x + 4`
    - Cubic: `x**3 - 3*x` (Local min & max)
    - Quartic: `x**4 - 2*x**2`
    """)
