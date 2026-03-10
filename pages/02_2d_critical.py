import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.title("🏔️ Critical Points in 2D")
st.markdown("Analyze functions of two variables $f(x, y)$ using the **Second Partial Derivative Test**.")

# ---------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------
st.sidebar.header("Function Settings")
func_str = st.sidebar.text_input("Formula f(x, y)", value="x**2 + y**2", help="Python/SymPy syntax (e.g., x**2 + y**2)")
grid_range = st.sidebar.slider("Plot Range", 1.0, 10.0, 3.0)

# =============================================================================
# CALCULATION & VISUALIZATION
# =============================================================================
if st.sidebar.button("Analyze Surface", type="primary", use_container_width=True):
    try:
        x, y = sp.symbols('x y')
        f_sym = sp.sympify(func_str)
        
        # Derivatives
        fx = sp.diff(f_sym, x)
        fy = sp.diff(f_sym, y)
        fxx = sp.diff(fx, x)
        fyy = sp.diff(fy, y)
        fxy = sp.diff(fx, y)
        
        # Critical points
        crit_points = sp.solve([fx, fy], (x, y))
        
        st.subheader("Partial Derivatives")
        st.latex(f"f_x = {sp.latex(fx)}")
        st.latex(f"f_y = {sp.latex(fy)}")
        
        st.markdown("---")
        
        results = []
        # Normalizing crit_points to a list of dicts/tuples
        if isinstance(crit_points, dict): crit_points = [crit_points]
        
        for p in crit_points:
            try:
                if isinstance(p, dict):
                    px, py = p[x], p[y]
                else:
                    px, py = p
                
                px_val = float(px.evalf())
                py_val = float(py.evalf())
                
                # Second Derivative Test (Discriminant D)
                fxx_val = float(fxx.subs({x: px_val, y: py_val}))
                fyy_val = float(fyy.subs({x: px_val, y: py_val}))
                fxy_val = float(fxy.subs({x: px_val, y: py_val}))
                
                D = fxx_val * fyy_val - fxy_val**2
                
                classification = "Inconclusive"
                if D > 0:
                    classification = "Local Minimum" if fxx_val > 0 else "Local Maximum"
                elif D < 0:
                    classification = "Saddle Point"
                
                results.append({
                    "x": round(px_val, 3),
                    "y": round(py_val, 3),
                    "D": round(D, 3),
                    "fxx": round(fxx_val, 3),
                    "Classification": classification
                })
            except Exception: continue
            
        if results:
            st.subheader("Classification Table")
            st.dataframe(results, use_container_width=True)
            
            # Plotting
            st.subheader("Contour Visualization")
            f_num = sp.lambdify((x, y), f_sym, 'numpy')
            xn = np.linspace(-grid_range, grid_range, 100)
            yn = np.linspace(-grid_range, grid_range, 100)
            X, Y = np.meshgrid(xn, yn)
            Z = f_num(X, Y)
            
            fig, ax = plt.subplots(figsize=(10, 7))
            cp = ax.contourf(X, Y, Z, levels=20, cmap="viridis", alpha=0.7)
            plt.colorbar(cp, label="f(x, y)")
            
            for res in results:
                color = "white" if res["Classification"] == "Local Minimum" else "black"
                marker = "o" if "Local" in res["Classification"] else "x"
                ax.plot(res["x"], res["y"], marker, color=color, markersize=10, label=f"{res['Classification']}")
            
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"Contours of $f(x, y) = {sp.latex(f_sym)}$")
            st.pyplot(fig)
        else:
            st.warning("No critical points found in this region.")
            
    except Exception as e:
        st.error(f"Error parsing function: {e}")
else:
    st.info("Enter a 2D function in the sidebar and click **Analyze Surface**.")
    st.markdown("""
    **Try these surfaces:**
    - Bowl: `x**2 + y**2`
    - Saddle: `x**2 - y**2`
    - Monkey Saddle: `x**3 - 3*x*y**2`
    """)
