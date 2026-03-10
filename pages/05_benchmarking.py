import streamlit as st
import numpy as np

st.title("📊 Optimization Benchmarking")
st.markdown("Benchmark gradient-based optimization algorithms on high-dimensional complex functions.")

# ---------------------------------------------------------------------
# Math Functions
# ---------------------------------------------------------------------
def rosenbrock(x):
    return sum(100.0*(x[i+1]-x[i]**2)**2 + (1-x[i])**2 for i in range(len(x)-1))

def rosenbrock_grad(x):
    n = len(x)
    g = np.zeros(n)
    for i in range(n-1):
        g[i] += -400*x[i]*(x[i+1]-x[i]**2) + 2*(x[i]-1)
        g[i+1] += 200*(x[i+1]-x[i]**2)
    return g

def rosenbrock_hess(x):
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n-1):
        H[i, i] += 1200*x[i]**2 - 400*x[i+1] + 2
        H[i, i+1] += -400*x[i]
        H[i+1, i] += -400*x[i]
        H[i+1, i+1] += 200
    return H

def ackley(x):
    n = len(x)
    a, b, c = 20, 0.2, 2*np.pi
    sum1 = np.sum(x**2)
    sum2 = np.sum(np.cos(c*x))
    return -a*np.exp(-b*np.sqrt(sum1/n)) - np.exp(sum2/n) + a + np.exp(1)

def ackley_grad(x):
    n = len(x)
    a, b, c = 20, 0.2, 2*np.pi
    sum1 = np.sum(x**2)
    sum2 = np.sum(np.cos(c*x))
    norm = np.sqrt(sum1/n)
    
    if norm < 1e-15:
        term1 = np.zeros(n)
    else:
        term1 = a*b*np.exp(-b*norm) * x / (n*norm)
    term2 = np.exp(sum2/n) * np.sin(c*x) * c / n
    return term1 + term2

def ackley_hess(x):
    n = len(x)
    H = np.zeros((n, n))
    eps = 1e-5
    g0 = ackley_grad(x)
    for i in range(n):
        x_plus = x.copy()
        x_plus[i] += eps
        g_plus = ackley_grad(x_plus)
        H[:, i] = (g_plus - g0) / eps
    return 0.5 * (H + H.T)

# ---------------------------------------------------------------------
# Algorithms
# ---------------------------------------------------------------------
def line_search(f, x, d, g, alpha=1.0, c=1e-4, rho=0.5):
    fx = f(x)
    slope = np.dot(g, d)
    if slope >= 0: return 1e-6
    while f(x + alpha * d) > fx + c * alpha * slope:
        alpha *= rho
        if alpha < 1e-12: break
    return alpha

def steepest_descent(f, grad, x0, tol=1e-6, max_iter=1000):
    x = x0.copy()
    for i in range(max_iter):
        g = grad(x)
        if np.linalg.norm(g) < tol: break
        d = -g
        alpha = line_search(f, x, d, g)
        x = x + alpha * d
    return x, f(x), i+1

def newton_method(f, grad, hess, x0, tol=1e-6, max_iter=1000):
    x = x0.copy()
    for i in range(max_iter):
        g = grad(x)
        if np.linalg.norm(g) < tol: break
        H = hess(x)
        try:
            eigvals = np.linalg.eigvalsh(H)
            if np.min(eigvals) <= 0:
                H = H + (abs(np.min(eigvals)) + 1e-4) * np.eye(len(x))
            d = np.linalg.solve(H, -g)
        except np.linalg.LinAlgError:
            d = -g
        alpha = line_search(f, x, d, g)
        x = x + alpha * d
    return x, f(x), i+1

def conjugate_gradient(f, grad, x0, tol=1e-6, max_iter=1000):
    x = x0.copy()
    g = grad(x)
    d = -g
    for i in range(max_iter):
        if np.linalg.norm(g) < tol: break
        alpha = line_search(f, x, d, g)
        x_next = x + alpha * d
        g_next = grad(x_next)
        
        beta = max(0, np.dot(g_next, g_next - g) / max(np.dot(g, g), 1e-15))
        d = -g_next + beta * d
        x, g = x_next, g_next
    return x, f(x), i+1

# ---------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------
st.sidebar.header("Benchmark Settings")

func_choice = st.sidebar.selectbox("Test Function", ["Rosenbrock Function", "Ackley Function"])
dimensions = st.sidebar.slider("Dimensions (n)", 2, 50, 10)
start_pt = st.sidebar.selectbox("Starting Point", ["Zeros (0, 0, ...)", "Ones (1, 1, ...)", "Far (2.0)"])

if st.sidebar.button("Run Benchmark Analysis", type="primary", use_container_width=True):
    with st.spinner(f"Running benchmarks on {func_choice} in {dimensions}D..."):
        if start_pt == "Zeros (0, 0, ...)":
            x0 = np.zeros(dimensions)
        elif start_pt == "Ones (1, 1, ...)":
            x0 = np.ones(dimensions)
        else:
            x0 = np.ones(dimensions) * 2.0
            
        if func_choice == "Rosenbrock Function":
            f, g, h = rosenbrock, rosenbrock_grad, rosenbrock_hess
        else:
            f, g, h = ackley, ackley_grad, ackley_hess
            
        def fmt_coord(x):
            if len(x) <= 4:
                return "(" + ", ".join(f"{v:.3f}" for v in x) + ")"
            return f"({x[0]:.3f}, {x[1]:.3f}, ..., {x[-1]:.3f})"
            
        results = []
        
        # Run SD
        x_sd, fval_sd, iter_sd = steepest_descent(f, g, x0)
        results.append({"Method": "Steepest Descent", "Iterations": iter_sd, "Final f(x)": fval_sd, "Minima": fmt_coord(x_sd)})
        
        # Run Newton
        x_nm, fval_nm, iter_nm = newton_method(f, g, h, x0)
        results.append({"Method": "Newton's Method", "Iterations": iter_nm, "Final f(x)": fval_nm, "Minima": fmt_coord(x_nm)})
        
        # Run CG
        x_cg, fval_cg, iter_cg = conjugate_gradient(f, g, x0)
        results.append({"Method": "Conjugate Gradient", "Iterations": iter_cg, "Final f(x)": fval_cg, "Minima": fmt_coord(x_cg)})
        
    st.subheader(f"Comparison: {func_choice} ({dimensions}D)")
    st.dataframe(results, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Key Observations")
    if func_choice == "Ackley Function":
        st.info("The Ackley function is highly non-convex. Gradient methods often get trapped in local minima unless the starting point is near (0,0).")
    else:
        st.info("The Rosenbrock function has a long, narrow parabolic valley. While the minimum is at (1,1,...), convergence can be slow for simple gradient descent.")

else:
    st.info("Select benchmark configurations from the sidebar and click 'Run Benchmark Analysis'.")
