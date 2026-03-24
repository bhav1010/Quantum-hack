import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import components as comp_vis

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Optical Bench Simulator", layout="wide")

st.title("🔬 Polarization Optical Bench Simulator")

# =========================
# SESSION STATE (store components)
# =========================
if "components" not in st.session_state:
    st.session_state.components = []

# =========================
# ADD COMPONENT BUTTONS
# =========================
st.subheader("➕ Add Components")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🟡 Polarizer"):
        st.session_state.components.append("Polarizer")

with c2:
    if st.button("🔵 QWP"):
        st.session_state.components.append("QWP")

with c3:
    if st.button("🟢 HWP"):
        st.session_state.components.append("HWP")

with c4:
    if st.button("🟣 Analyzer"):
        st.session_state.components.append("Analyzer")

if st.button("🔄 Reset System"):
    st.session_state.components = []

# =========================
# INPUT LIGHT
# =========================
st.subheader("🔴 Input Laser")

Ax = st.slider("Ex Amplitude", 0.1, 2.0, 1.0)
Ay = st.slider("Ey Amplitude", 0.1, 2.0, 1.0)
delta = st.slider("Phase Difference δ (radians)", 0.0, 2*np.pi, 0.0)

# Initial Jones Vector
J = np.array([[Ax],
              [Ay * np.exp(1j * delta)]])

# =========================
# PHYSICS FUNCTIONS
# =========================
def rotation(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

def waveplate(phase, theta):
    R = rotation(theta)
    R_inv = rotation(-theta)
    W = np.array([
        [1, 0],
        [0, np.exp(1j * phase)]
    ])
    return R_inv @ W @ R

def polarizer(theta):
    return np.array([
        [np.cos(theta)**2, np.cos(theta)*np.sin(theta)],
        [np.cos(theta)*np.sin(theta), np.sin(theta)**2]
    ])

# =========================
# VISUAL OPTICAL BENCH
# =========================
st.subheader("🧱 Interactive Optical Bench")

# Build the HTML content for the iframe
bench_content = comp_vis.get_bench_styles()
bench_content += '<div class="bench-container">'

# 1. Laser
bench_content += f'<div class="component-box">{comp_vis.get_laser_svg()}</div>'

# 2. Initial Beam
I_curr = np.abs(J[0][0])**2 + np.abs(J[1][0])**2
Ax_curr = np.abs(J[0][0])
Ay_curr = np.abs(J[1][0])
delta_curr = np.angle(J[1][0]) - np.angle(J[0][0])

state_svg = comp_vis.get_polarization_state_svg(Ax_curr, Ay_curr, delta_curr, I_curr)
bench_content += comp_vis.get_beam_segment_html(I_curr, state_svg)

M_total = np.eye(2)
J_current = J.copy()

# 3. Components
for i, comp in enumerate(st.session_state.components):
    angle = st.sidebar.slider(f"Angle (°) - {comp} {i}", 0, 180, 0, key=f"angle_{i}")
    theta = np.radians(angle)
    
    color = "#ffcc00"
    if comp == "QWP": color = "#3399ff"
    elif comp == "HWP": color = "#33cc33"
    elif comp == "Analyzer": color = "#cc33ff"

    if comp in ["Polarizer", "Analyzer"]:
        M = polarizer(theta)
    elif comp == "QWP":
        M = waveplate(np.pi/2, theta)
    elif comp == "HWP":
        M = waveplate(np.pi, theta)
    else:
        M = np.eye(2)

    M_total = M @ M_total
    J_current = M @ J_current
    
    I_curr = np.abs(J_current[0][0])**2 + np.abs(J_current[1][0])**2
    Ax_curr = np.abs(J_current[0][0])
    Ay_curr = np.abs(J_current[1][0])
    delta_curr = np.angle(J_current[1][0]) - np.angle(J_current[0][0])

    bench_content += f'<div class="component-box">{comp_vis.get_component_svg(comp, angle, color)}</div>'
    state_svg = comp_vis.get_polarization_state_svg(Ax_curr, Ay_curr, delta_curr, I_curr)
    bench_content += comp_vis.get_beam_segment_html(I_curr, state_svg)

# 4. Detector
bench_content += f'<div class="component-box">{comp_vis.get_detector_svg(I_curr)}</div>'
bench_content += '</div>'

# Render in an iframe for best SVG compatibility
st.components.v1.html(bench_content, height=350, scrolling=True)

st.write("---")

# =========================
# RESULTS & GRAPHS
# =========================
# Modified ratio: Bench area is already handled above, now we show graphs clearly
res_col1, res_col2 = st.columns([1, 1.2])

J_out = J_current
Ax_out = np.abs(J_out[0][0])
Ay_out = np.abs(J_out[1][0])
delta_out = np.angle(J_out[1][0]) - np.angle(J_out[0][0])
intensity = Ax_out**2 + Ay_out**2

with res_col1:
    st.subheader("📊 Output Analysis")
    st.write(f"### Intensity: {intensity:.3f}")
    # Refined Classification (Robust to zero amplitudes)
    is_linear = False
    if Ax_out < 0.05 or Ay_out < 0.05:
        is_linear = True
    elif abs(delta_out % np.pi) < 0.08 or abs(delta_out % np.pi) > (np.pi - 0.08):
        is_linear = True
        
    if is_linear:
        st.success("Linear Polarization")
    elif abs(Ax_out - Ay_out) < 0.08 and abs(abs(delta_out % np.pi) - np.pi/2) < 0.08:
        st.success("Circular Polarization")
    else:
        st.warning("Elliptical Polarization")
    
    st.write(f"**Ax** = {Ax_out:.2f}, **Ay** = {Ay_out:.2f}")
    st.write(f"**Phase Diff** = {np.degrees(delta_out):.2f}°")
    st.latex(r"I = |E_x|^2 + |E_y|^2")

with res_col2:
    st.subheader("📈 Polarization Ellipse")
    t = np.linspace(0, 2*np.pi, 500)
    Ex = Ax_out * np.cos(t)
    Ey = Ay_out * np.cos(t + delta_out)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.plot(Ex, Ey, color='red', lw=2.5)
    ax.set_aspect('equal')
    ax.set_xlim([-2.2, 2.2]); ax.set_ylim([-2.2, 2.2])
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_title("E-Field Trace", fontsize=10)
    st.pyplot(fig)