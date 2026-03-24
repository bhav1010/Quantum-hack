import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Polarization Optics Virtual Lab")

# User Inputs
Ax = st.slider("Amplitude Ex", 0.1, 1.0, 1.0)
Ay = st.slider("Amplitude Ey", 0.1, 1.0, 1.0)
delta = st.slider("Phase Difference (radians)", 0.0, np.pi, 0.0)

# Time
t = np.linspace(0, 2*np.pi, 500)

Ex = Ax * np.cos(t)
Ey = Ay * np.cos(t + delta)

# Plot
fig, ax = plt.subplots()
ax.plot(Ex, Ey)
ax.set_title("Polarization State")
ax.set_xlabel("Ex")
ax.set_ylabel("Ey")
ax.grid()

st.pyplot(fig)

# Learning Output
if delta == 0:
    st.success("Linear Polarization")
elif abs(delta - np.pi/2) < 0.1:
    st.success("Circular Polarization")
else:
    st.success("Elliptical Polarization")