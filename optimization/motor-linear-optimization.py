import numpy as np
from scipy.optimize import linprog

# Sample power consumption functions: P1(x1) = c1 * x1, P2(x2) = c2 * x2
c1, c2 = 10, 20

# Operating speed constraints
x1_min, x1_max = 0, 100
x2_min, x2_max = 0, 50

# Define the coefficients for the objective function
c = [c1, c2]

# Define the inequality constraints matrix and vector
A = [[1, 0], [0, 1], [-1, 0], [0, -1]]
b = [x1_max, x2_max, -x1_min, -x2_min]

# Solve the linear programming problem
result = linprog(c, A_ub=A, b_ub=b)

# Extract the optimal solution
optimal_solution = result.x

print("Optimal solution:", optimal_solution)