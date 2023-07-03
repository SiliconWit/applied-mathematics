import numpy as np
import matplotlib.pyplot as plt

def solve_heat_equation(L, T, alpha, N, M, f):
    # Parameters
    h = L / N
    k = T / M

    # Create grid points
    x = np.linspace(0, L, N+1)

    # Create initial temperature distribution
    u0 = f(x)

    # Create coefficient matrices
    A = np.zeros((N-1, N-1))
    B = np.zeros((N-1, N-1))

    # Populate the coefficient matrices
    A[0, 0] = 1 + alpha * k / (2 * h**2)
    A[0, 1] = -alpha * k / (2 * h**2)
    B[0, 0] = 1 - alpha * k / (2 * h**2)
    B[0, 1] = alpha * k / (2 * h**2)

    for i in range(1, N-2):
        A[i, i-1] = -alpha * k / (2 * h**2)
        A[i, i] = 1 + alpha * k / h**2
        A[i, i+1] = -alpha * k / (2 * h**2)

        B[i, i-1] = alpha * k / (2 * h**2)
        B[i, i] = 1 - alpha * k / h**2
        B[i, i+1] = alpha * k / (2 * h**2)

    A[N-2, N-3] = -alpha * k / (2 * h**2)
    A[N-2, N-2] = 1 + alpha * k / h**2
    B[N-2, N-3] = alpha * k / (2 * h**2)
    B[N-2, N-2] = 1 - alpha * k / h**2

    # Initialize solution matrix
    U = np.zeros((N+1, M+1))
    U[:, 0] = u0

    # Solve the system iteratively
    for j in range(M):
        # Use matrix solver to find U at the next time step
        U[1:N, j+1] = np.linalg.solve(A, np.dot(B, U[1:N, j]))

    return x, U

# Example usage
L = 1.0
T = 0.5
alpha = 0.1
N = 100  # Number of spatial grid points
M = 1000  # Number of time steps

# Define initial temperature distribution function
def f(x):
    # Heat at one end (e.g., candle)
    heat_location = 0.2 * L  # Specify the location of heat
    heat_strength = 10.0  # Adjust the strength of heat

    # Calculate the initial temperature distribution
    initial_temperature = np.exp(-((x - heat_location) ** 2) / 0.01)
    initial_temperature *= heat_strength

    return initial_temperature

x, U = solve_heat_equation(L, T, alpha, N, M, f)

# Plot the results using color map and annotations
plt.figure()
X, T = np.meshgrid(x, np.linspace(T, 0, M+1))
plt.pcolormesh(X, T, U.T, shading='auto', cmap='hot')
plt.colorbar(label='Temperature')
plt.xlabel('x')
plt.ylabel('Time')
plt.title('Temperature Distribution')
plt.grid(True)
plt.savefig("1d-heat-distribution.png")
plt.show()