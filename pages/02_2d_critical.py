import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

st.title("🏔️ Critical Points in 2D")
st.markdown("Analyze functions of two variables $f(x, y)$ using the Second Partial Derivative (Hessian) Test.")

st.sidebar.header("Function Input")
expr_string = st.sidebar.text_input("Enter f(x, y):", value="2*x*y + 2*x - x**2 - 2*y**2")

x_min = st.sidebar.number_input("Plot X Min", value=-5.0)
x_max = st.sidebar.number_input("Plot X Max", value=5.0)
y_min = st.sidebar.number_input("Plot Y Min", value=-5.0)
y_max = st.sidebar.number_input("Plot Y Max", value=5.0)

try:
    x, y = sp.symbols('x y')
    f = sp.sympify(expr_string)
    
    st.markdown(f"**Function:** $\\quad f(x, y) = {sp.latex(f)}$")
    
    # 1. Compute Gradient
    f_x = sp.diff(f, x)
    f_y = sp.diff(f, y)
    
    col1, col2 = st.columns(2)
    col1.markdown(f"**$\\frac{{\\partial f}}{{\\partial x}}$ =** $\\quad {sp.latex(f_x)}$")
    col2.markdown(f"**$\\frac{{\\partial f}}{{\\partial y}}$ =** $\\quad {sp.latex(f_y)}$")
    
    with st.spinner("Finding critical points and computing Hessian..."):
        gradient = [f_x, f_y]
        critical_points = sp.solve(gradient, (x, y), dict=True)
        hessian = sp.hessian(f, (x, y))
        
    st.markdown(f"**Hessian Matrix $H$:** $\\quad {sp.latex(hessian)}$")
    
    if not critical_points:
        st.warning("No real critical points found.")
    else:
        st.subheader("Critical Points Analysis")
        results = []
        
        for pt in critical_points:
            # Check if point values are real numbers
            if not all(val.is_real for val in pt.values()):
                continue
                
            x_val, y_val = pt.get(x, 0), pt.get(y, 0)
            
            # Evaluate Hessian
            h_eval = hessian.subs({x: x_val, y: y_val})
            det_h = h_eval.det()
            f_xx = h_eval[0, 0]
            
            # Classification
            if det_h > 0:
                if f_xx > 0:
                    classification = "Local Minimum"
                else:
                    classification = "Local Maximum"
            elif det_h < 0:
                classification = "Saddle Point"
            else:
                classification = "Inconclusive"
                
            f_val = f.subs({x: x_val, y: y_val}).evalf()
            
            results.append({
                "x": float(x_val.evalf()),
                "y": float(y_val.evalf()),
                "f(x, y)": float(f_val),
                "Determinant |H|": float(det_h.evalf()),
                "f_xx": float(f_xx.evalf()),
                "Classification": classification
            })
            
        if results:
            st.dataframe(results, use_container_width=True)
            
            # Contour Plot Visualization
            st.subheader("Contour Plot")
            
            f_num = sp.lambdify((x, y), f, "numpy")
            
            X, Y = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
            
            # In case the function is a constant
            try:
                Z = f_num(X, Y)
                if np.isscalar(Z):
                    Z = np.full_like(X, Z)
            except Exception:
                # Fallback for complex functions if lambdify fails
                Z = np.zeros_like(X)
                for i in range(X.shape[0]):
                    for j in range(X.shape[1]):
                        Z[i, j] = float(f.subs({x: X[i, j], y: Y[i, j]}).evalf())
            
            fig, ax = plt.subplots(figsize=(8, 6))
            cp = ax.contourf(X, Y, Z, levels=30, cmap="viridis", alpha=0.8)
            ax.contour(X, Y, Z, levels=30, colors='black', linewidths=0.5, alpha=0.3)
            fig.colorbar(cp, ax=ax, label="f(x, y)")
            
            for res in results:
                cx, cy = res["x"], res["y"]
                cls = res["Classification"]
                color = "white" if "Minimum" in cls else "red" if "Maximum" in cls else "orange"
                ax.scatter([cx], [cy], color=color, s=100, edgecolors='black', label=f"{cls} at ({cx:.1f}, {cy:.1f})")
                
            ax.set_title("2D Contour Plot")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            
            handles, labels = ax.get_legend_handles_labels()
            if handles:
                by_label = dict(zip(labels, handles))
                ax.legend(by_label.values(), by_label.keys(), loc="upper right")
                
            st.pyplot(fig)
        else:
            st.warning("No real critical points found (only complex).")

except Exception as e:
    st.error(f"Error parsing or evaluating the function: {e}")
