import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

st.title("📉 Unconstrained Minimization")
st.markdown("Compare gradient-based optimization algorithms: **Steepest Descent**, **Newton's Method**, and **Conjugate Gradient**.")

# -------------------------------------------------------------
# Input Section
# -------------------------------------------------------------
st.sidebar.header("Optimization Parameters")
func_str = st.sidebar.text_input("Enter f(x, y):", value="(x**2 + y - 11)**2 + (x + y**2 - 7)**2")
start_x = st.sidebar.number_input("Starting x", value=2.0)
start_y = st.sidebar.number_input("Starting y", value=2.0)
start_pt = np.array([start_x, start_y])

algorithm = st.sidebar.selectbox("Select Algorithm", ["All (Compare)", "Steepest Descent", "Newton's Method", "Conjugate Gradient"])

cg_beta = "FR"
if algorithm in ["All (Compare)", "Conjugate Gradient"]:
    cg_beta = st.sidebar.radio("CG Beta Method", ["Fletcher-Reeves (FR)", "Polak-Ribiere (PR)"])
    cg_beta = "FR" if "FR" in cg_beta else "PR"

max_iter = st.sidebar.slider("Max Iterations", 10, 500, 100)
tol = st.sidebar.number_input("Tolerance (Gradient Norm)", value=1e-6, format="%e")

x_lim = st.sidebar.slider("Plot X Range", -10.0, 10.0, (-6.0, 6.0))
y_lim = st.sidebar.slider("Plot Y Range", -10.0, 10.0, (-6.0, 6.0))
contour_levels = st.sidebar.slider("Contour Levels", 10, 100, 50)

if st.sidebar.button("Run Optimizer"):
    try:
        with st.spinner("Optimizing..."):
            # 1. Symbolic Parsing
            x_sym, y_sym = sp.symbols("x y")
            f_sym = sp.sympify(func_str)
            
            # Calculate Gradient and Hessian
            grad_sym = [sp.diff(f_sym, var) for var in (x_sym, y_sym)]
            hess_sym = [[sp.diff(g, var) for var in (x_sym, y_sym)] for g in grad_sym]
            
            # Numerical Functions
            f_func = sp.lambdify((x_sym, y_sym), f_sym, 'numpy')
            grad_func = sp.lambdify((x_sym, y_sym), grad_sym, 'numpy')
            hess_func = sp.lambdify((x_sym, y_sym), hess_sym, 'numpy')
            
            f = lambda v: f_func(v[0], v[1])
            grad = lambda v: np.array(grad_func(v[0], v[1]), dtype=float)
            hess = lambda v: np.array(hess_func(v[0], v[1]), dtype=float)

            # 2. Line Search (Backtracking)
            def line_search(x_vec, d, g):
                alpha = 1.0
                c, rho = 1e-4, 0.5
                while f(x_vec + alpha * d) > f(x_vec) + c * alpha * np.dot(g, d):
                    alpha *= rho
                    if alpha < 1e-10: break
                return alpha

            # 3. Solvers
            def run_sd():
                curr = start_pt.copy()
                path = [curr]
                for _ in range(max_iter):
                    g = grad(curr)
                    if np.linalg.norm(g) < tol: break
                    d = -g
                    alpha = line_search(curr, d, g)
                    curr = curr + alpha * d
                    path.append(curr)
                return np.array(path)

            def run_nm():
                curr = start_pt.copy()
                path = [curr]
                for _ in range(max_iter):
                    g = grad(curr)
                    if np.linalg.norm(g) < tol: break
                    H = hess(curr)
                    try:
                        d = np.linalg.solve(H, -g)
                    except np.linalg.LinAlgError:
                        d = -g  # Fallback to steepest descent
                    alpha = line_search(curr, d, g)
                    curr = curr + alpha * d
                    path.append(curr)
                return np.array(path)

            def run_cg(beta_method):
                curr = start_pt.copy()
                path = [curr]
                g = grad(curr)
                d = -g
                for _ in range(max_iter):
                    if np.linalg.norm(g) < tol: break
                    alpha = line_search(curr, d, g)
                    curr_next = curr + alpha * d
                    path.append(curr_next)
                    
                    g_next = grad(curr_next)
                    
                    if beta_method == "PR":
                        beta = max(0.0, np.dot(g_next, g_next - g) / max(np.dot(g, g), 1e-15))
                    else:
                        beta = max(0.0, np.dot(g_next, g_next) / max(np.dot(g, g), 1e-15))
                    
                    d = -g_next + beta * d
                    curr, g = curr_next, g_next
                return np.array(path)

            paths = {}
            if algorithm in ["All (Compare)", "Steepest Descent"]:
                paths["Steepest Descent"] = run_sd()
            if algorithm in ["All (Compare)", "Newton's Method"]:
                paths["Newton's Method"] = run_nm()
            if algorithm in ["All (Compare)", "Conjugate Gradient"]:
                paths[f"Conjugate Gradient ({cg_beta})"] = run_cg(cg_beta)

            # 4. Results Table
            st.subheader("Optimization Results")
            results = []
            for name, p in paths.items():
                results.append({
                    "Algorithm": name,
                    "Iterations": len(p)-1,
                    "Final f(x, y)": f"{f(p[-1]):.6f}",
                    "Final x": f"{p[-1][0]:.6f}",
                    "Final y": f"{p[-1][1]:.6f}"
                })
            st.dataframe(results, use_container_width=True)

            # 5. Visualization
            st.subheader("Convergence Path on Contour Plot")
            x_range = np.linspace(x_lim[0], x_lim[1], 200)
            y_range = np.linspace(y_lim[0], y_lim[1], 200)
            X, Y = np.meshgrid(x_range, y_range)
            Z = f_func(X, Y)

            fig, ax = plt.subplots(figsize=(10, 8))
            contours = ax.contour(X, Y, Z, levels=contour_levels, cmap='viridis')
            ax.clabel(contours, inline=True, fontsize=10, fmt='%.1f')
            
            colors = {"Steepest Descent": 'ro-', "Newton's Method": 'bx--', f"Conjugate Gradient ({cg_beta})": 'g*-'}
            
            for name, p in paths.items():
                ax.plot(p[:,0], p[:,1], colors.get(name, 'mo-'), label=f'{name} ({len(p)-1} iters)', alpha=0.8)

            ax.plot(start_pt[0], start_pt[1], 'k^', markersize=10, label=f'Start {tuple(start_pt)}')

            ax.set_title(f"Optimization: $f(x, y) = {func_str}$")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend(loc="upper right")
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
            
    except Exception as e:
        st.error(f"Error during optimization: {e}")
else:
    st.info("Configured your parameters in the sidebar and click 'Run Optimizer'.")
