import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Polarization Optics Lab", layout="centered")

st.title("Polarization Optics Virtual Lab")

# ============================
# Sidebar
# ============================
experiment = st.sidebar.selectbox(
    "Choose Experiment",
    ["Polarizer (Malus Law)", "Polarization Conversion"]
)

# ============================
# HELPER FUNCTIONS
# ============================

def rotation(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta),  np.cos(theta)]
    ])

def jones_waveplate(phase, theta):
    R = rotation(theta)
    R_inv = rotation(-theta)
    W = np.array([
        [1, 0],
        [0, np.exp(1j * phase)]
    ])
    return R_inv @ W @ R

def jones_polarizer(theta):
    return np.array([
        [np.cos(theta)**2, np.cos(theta)*np.sin(theta)],
        [np.cos(theta)*np.sin(theta), np.sin(theta)**2]
    ])

def stokes(J):
    Ex = J[0][0]
    Ey = J[1][0]
    S0 = np.abs(Ex)**2 + np.abs(Ey)**2
    S1 = np.abs(Ex)**2 - np.abs(Ey)**2
    S2 = 2*np.real(Ex*np.conj(Ey))
    S3 = -2*np.imag(Ex*np.conj(Ey))
    return S0, S1, S2, S3

# ============================
# EXPERIMENT 1: MALUS LAW
# ============================
if experiment == "Polarizer (Malus Law)":

    st.header("Polarizer Working Principle")

    theta0 = st.slider("Input Angle θ₀ (deg)", 0, 180, 0)
    theta = st.slider("Polarizer Angle θ (deg)", 0, 180, 45)

    theta0_rad = np.radians(theta0)
    theta_rad = np.radians(theta)

    I = (np.cos(theta_rad - theta0_rad))**2

    st.write(f"### Output Intensity: {I:.3f}")

    angles = np.linspace(0, np.pi, 200)
    intensity = (np.cos(angles - theta0_rad))**2

    fig, ax = plt.subplots()
    ax.plot(np.degrees(angles), intensity)
    ax.set_xlabel("Angle (deg)")
    ax.set_ylabel("Intensity")
    ax.set_title("Malus Law")
    ax.grid()

    st.pyplot(fig)

    st.latex(r"I = I_0 \cos^2(\theta - \theta_0)")


# ============================
# EXPERIMENT 2: CONVERSION
# ============================
elif experiment == "Polarization Conversion":

    st.header("Polarization Conversion (Jones Calculus)")

    mode = st.radio("Input Mode", ["Preset", "Custom"])

    # INPUT STATE
    if mode == "Preset":
        pol = st.selectbox("Input Polarization", ["Linear", "Circular"])

        if pol == "Linear":
            Ax, Ay, delta = 1, 1, 0
        else:
            Ax, Ay, delta = 1, 1, np.pi/2

    else:
        Ax = st.slider("Amplitude Ex", 0.1, 2.0, 1.0)
        Ay = st.slider("Amplitude Ey", 0.1, 2.0, 1.0)
        delta = st.slider("Phase Difference δ", 0.0, 2*np.pi, 0.0)

    # COMPONENT CHAIN
    component = st.selectbox("Optical Component", ["None", "Polarizer", "QWP", "HWP"])
    angle_deg = st.slider("Component Orientation (deg)", 0, 180, 0)
    angle = np.radians(angle_deg)

    # JONES VECTOR
    J = np.array([[Ax],
                  [Ay * np.exp(1j * delta)]])

    # APPLY COMPONENT
    if component == "Polarizer":
        M = jones_polarizer(angle)
    elif component == "QWP":
        M = jones_waveplate(np.pi/2, angle)
    elif component == "HWP":
        M = jones_waveplate(np.pi, angle)
    else:
        M = np.eye(2)

    J_out = M @ J

    # EXTRACT VALUES
    Ax_out = np.abs(J_out[0][0])
    Ay_out = np.abs(J_out[1][0])
    delta_out = np.angle(J_out[1][0]) - np.angle(J_out[0][0])

    # PLOT
    t = np.linspace(0, 2*np.pi, 500)
    Ex = Ax_out * np.cos(t)
    Ey = Ay_out * np.cos(t + delta_out)

    fig, ax = plt.subplots()
    ax.plot(Ex, Ey)
    ax.set_title("Output Polarization")
    ax.set_xlabel("Ex")
    ax.set_ylabel("Ey")
    ax.grid()

    st.pyplot(fig)

    # CLASSIFY
    if abs(delta_out % np.pi) < 0.1:
        st.success("Linear Polarization")
    elif abs((delta_out - np.pi/2) % np.pi) < 0.1:
        st.success("Circular Polarization")
    else:
        st.success("Elliptical Polarization")

    # STOKES PARAMETERS
    S0, S1, S2, S3 = stokes(J_out)

    st.markdown("### Stokes Parameters")
    st.write(f"S0 = {S0:.2f}")
    st.write(f"S1 = {S1:.2f}")
    st.write(f"S2 = {S2:.2f}")
    st.write(f"S3 = {S3:.2f}")

    # SHOW PARAMETERS
    st.markdown("### Output Parameters")
    st.write(f"Ax = {Ax_out:.2f}, Ay = {Ay_out:.2f}")
    st.write(f"Phase Difference = {delta_out:.2f} rad")

    st.latex(r"E_x = A_x \cos(\omega t)")
    st.latex(r"E_y = A_y \cos(\omega t + \delta)")