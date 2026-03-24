import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# Create output folder
output_folder = "polarization_gifs"
os.makedirs(output_folder, exist_ok=True)

# Time array
t = np.linspace(0, 2*np.pi, 300)

# Function to generate animation and save GIF
def create_gif(Ax, Ay, delta, title, filename):
    fig, ax = plt.subplots()

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_title(title)
    ax.set_xlabel("Ex")
    ax.set_ylabel("Ey")
    ax.grid()

    line, = ax.plot([], [], lw=2)
    point, = ax.plot([], [], 'ro')

    def init():
        line.set_data([], [])
        point.set_data([], [])
        return line, point

    def update(frame):
        Ex = Ax * np.cos(t[:frame])
        Ey = Ay * np.cos(t[:frame] + delta)

        line.set_data(Ex, Ey)

        # Moving point
        Ex_point = Ax * np.cos(t[frame])
        Ey_point = Ay * np.cos(t[frame] + delta)
        point.set_data([Ex_point], [Ey_point])

        return line, point

    ani = FuncAnimation(fig, update, frames=len(t),
                        init_func=init, interval=20, blit=True)

    filepath = os.path.join(output_folder, filename)
    ani.save(filepath, writer='pillow')

    plt.close(fig)
    print(f"Saved: {filepath}")


# -------------------------
# Generate All Cases
# -------------------------

# 1. Linear Polarization
create_gif(
    Ax=1,
    Ay=1,
    delta=0,
    title="Linear Polarization",
    filename="linear.gif"
)

# 2. Circular Polarization
create_gif(
    Ax=1,
    Ay=1,
    delta=np.pi/2,
    title="Circular Polarization",
    filename="circular.gif"
)

# 3. Elliptical Polarization
create_gif(
    Ax=1,
    Ay=0.5,
    delta=np.pi/3,
    title="Elliptical Polarization",
    filename="elliptical.gif"
)

print("\nAll GIFs generated successfully!")