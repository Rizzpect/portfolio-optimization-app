import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

st.title("📉 Unconstrained Minimization")
st.markdown("Compare **Steepest Descent**, **Newton's Method**, and **Conjugate Gradient** on any custom 2D function.")

# ---------------------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------------------
st.sidebar.header("Optimization Settings")

func_str = st.sidebar.text_input("Formula f(x, y)", value="x**2 + 5*y**2", help="Python/SymPy syntax (e.g., x**2 + y**2)")
col1, col2 = st.sidebar.columns(2)
x0_val = col1.number_input("Start x", value=2.0)
y0_val = col2.number_input("Start y", value=2.0)

tol = st.sidebar.select_slider("Tolerance", options=[1e-3, 1e-4, 1e-5, 1e-6], value=1e-6)
max_iter = st.sidebar.slider("Max Iterations", 10, 500, 100)

st.sidebar.markdown("---")
st.sidebar.header("Plotting Range")
grid_range = st.sidebar.slider("View Range", 1.0, 20.0, 5.0)

# =============================================================================
# CORE MATH LOGIC
# =============================================================================
def build_solvers(func_str):
    x_s, y_s = sp.symbols("x y")
    f_sym = sp.sympify(func_str)
    
    grad_sym = [sp.diff(f_sym, v) for v in (x_s, y_s)]
    hess_sym = [[sp.diff(g, v) for v in (x_s, y_s)] for g in grad_sym]
    
    f_num = sp.lambdify((x_s, y_s), f_sym, "numpy")
    grad_num = sp.lambdify((x_s, y_s), grad_sym, "numpy")
    hess_num = sp.lambdify((x_s, y_s), hess_sym, "numpy")
    
    def f(v): return float(f_num(v[0], v[1]))
    def grad(v): return np.array(grad_num(v[0], v[1]), dtype=float).flatten()
    def hess(v): return np.array(hess_num(v[0], v[1]), dtype=float)
    
    return f, grad, hess, f_num

def backtrack(f, x, d, g, c=1e-4, rho=0.5):
    alpha = 1.0
    fx = f(x)
    dg = np.dot(g, d)
    while f(x + alpha * d) > fx + c * alpha * dg:
        alpha *= rho
        if alpha < 1e-12: break
    return alpha

def run_sd(f, grad, start, tol, iters):
    path = [start.copy()]
    x = start.copy()
    for _ in range(iters):
        g = grad(x)
        if np.linalg.norm(g) < tol: break
        d = -g
        alpha = backtrack(f, x, d, g)
        x = x + alpha * d
        path.append(x.copy())
    return np.array(path)

def run_newton(f, grad, hess, start, tol, iters):
    path = [start.copy()]
    x = start.copy()
    for _ in range(iters):
        g = grad(x)
        if np.linalg.norm(g) < tol: break
        H = hess(x)
        try:
            d = np.linalg.solve(H, -g)
        except np.linalg.LinAlgError:
            d = -g
        alpha = backtrack(f, x, d, g)
        x = x + alpha * d
        path.append(x.copy())
    return np.array(path)

def run_cg(f, grad, start, tol, iters):
    path = [start.copy()]
    x = start.copy()
    g = grad(x)
    d = -g.copy()
    for _ in range(iters):
        if np.linalg.norm(g) < tol: break
        alpha = backtrack(f, x, d, g)
        x_new = x + alpha * d
        g_new = grad(x_new)
        denom = np.dot(g, g)
        beta = max(0.0, np.dot(g_new, g_new) / denom) if denom > 1e-14 else 0.0
        d = -g_new + beta * d
        x, g = x_new, g_new
        path.append(x.copy())
    return np.array(path)

# =============================================================================
# UI EXECUTION
# =============================================================================
if st.sidebar.button("Execute Solvers", type="primary", use_container_width=True):
    start_pt = np.array([x0_val, y0_val])
    try:
        f, grad, hess, f_num = build_solvers(func_str)
        
        with st.spinner("Calculating paths..."):
            sd_path = run_sd(f, grad, start_pt, tol, max_iter)
            nm_path = run_newton(f, grad, hess, start_pt, tol, max_iter)
            cg_path = run_cg(f, grad, start_pt, tol, max_iter)
            
        # Summary Metrics
        st.subheader("Performance Summary")
        m1, m2, m3 = st.columns(3)
        m1.metric("Steepest Descent", f"{f(sd_path[-1]):.4e}", f"{len(sd_path)-1} iters")
        m2.metric("Newton's Method", f"{f(nm_path[-1]):.4e}", f"{len(nm_path)-1} iters")
        m3.metric("Conjugate Gradient", f"{f(cg_path[-1]):.4e}", f"{len(cg_path)-1} iters")
        
        # Convergence Plot
        st.subheader("Gradient Norm Convergence")
        fig_conv, ax_conv = plt.subplots(figsize=(10, 3))
        ax_conv.semilogy([np.linalg.norm(grad(p)) for p in sd_path], label="SD", color="red")
        ax_conv.semilogy([np.linalg.norm(grad(p)) for p in nm_path], label="Newton", color="blue")
        ax_conv.semilogy([np.linalg.norm(grad(p)) for p in cg_path], label="CG", color="green")
        ax_conv.set_ylabel("||grad||")
        ax_conv.set_xlabel("Iteration")
        ax_conv.legend()
        ax_conv.grid(True, alpha=0.3)
        st.pyplot(fig_conv)

        # Trajectory Plot
        st.subheader("Optimization Trajectories")
        x_mesh = np.linspace(-grid_range, grid_range, 100)
        y_mesh = np.linspace(-grid_range, grid_range, 100)
        X, Y = np.meshgrid(x_mesh, y_mesh)
        Z = f_num(X, Y)
        
        fig, ax = plt.subplots(figsize=(10, 7))
        cp = ax.contourf(X, Y, Z, levels=20, cmap="viridis", alpha=0.6)
        plt.colorbar(cp, label="f(x, y)")
        
        ax.plot(sd_path[:, 0], sd_path[:, 1], 'ro-', label="SD", markersize=3, alpha=0.7)
        ax.plot(nm_path[:, 0], nm_path[:, 1], 'bx-', label="Newton", markersize=4, alpha=0.7)
        ax.plot(cg_path[:, 0], cg_path[:, 1], 'g*-', label="CG", markersize=4, alpha=0.7)
        ax.plot(x0_val, y0_val, 'ks', markersize=8, label="Start")
        
        ax.set_title(f"Minimizing: $f(x, y) = {sp.latex(sp.sympify(func_str))}$")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error executing optimization: {e}")
else:
    st.info("Set the function and parameters in the sidebar and click **Execute Solvers**.")
    st.markdown("""
    **Test some classic functions:**
    - Quadratic: `x**2 + 10*y**2`
    - Banana (Rosenbrock): `(1-x)**2 + 100*(y-x**2)**2`
    - Non-convex: `x**4 + y**4 - 4*x*y`
    """)
