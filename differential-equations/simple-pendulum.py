import numpy as np
import matplotlib.pyplot as plt

# Define the ODEs
def pendulum_ode(t, y, g, l):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = -(g / l) * np.sin(theta)
    return [dtheta_dt, domega_dt]

# Define the simulation parameters
g = 9.81
l = 1.0
t = np.linspace(0, 10, 1000)
y0 = [np.pi/4, 0]

# Use the Runge-Kutta method to simulate the motion of the pendulum
sol = np.zeros((len(t), 2))
sol[0] = y0
for i in range(len(t) - 1):
    h = t[i+1] - t[i]
    k1 = h * np.array(pendulum_ode(t[i], sol[i], g, l))
    k2 = h * np.array(pendulum_ode(t[i] + h/2, sol[i] + k1/2, g, l))
    k3 = h * np.array(pendulum_ode(t[i] + h/2, sol[i] + k2/2, g, l))
    k4 = h * np.array(pendulum_ode(t[i] + h, sol[i] + k3, g, l))
    sol[i+1] = sol[i] + (k1 + 2*k2 + 2*k3 + k4) / 6

# Plot the results
plt.plot(t, sol[:, 0])
plt.xlabel('Time (s)')
plt.ylabel('Angle (rad)')
plt.show()