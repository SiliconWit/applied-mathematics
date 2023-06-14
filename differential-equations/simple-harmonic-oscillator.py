import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def simple_harmonic_oscillator(y, t, omega_n, zeta, f):
    x, x_dot = y
    x_dot_dot = -2 * zeta * omega_n * x_dot - omega_n ** 2 * x + f(t)
    return [x_dot, x_dot_dot]

def simulate_oscillator(omega_n, zeta, f, x0, x_dot0, t):
    y0 = [x0, x_dot0]
    y = odeint(simple_harmonic_oscillator, y0, t, args=(omega_n, zeta, f))
    return y[:, 0], y[:, 1]

def sin_force(t):
    return np.sin(2 * np.pi * t)

omega_n = 10
zeta = 0.2
x0 = 0
x_dot0 = 0
t = np.linspace(0, 10, 1000)

x, x_dot = simulate_oscillator(omega_n, zeta, sin_force, x0, x_dot0, t)

plt.plot(t, x)
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.show()