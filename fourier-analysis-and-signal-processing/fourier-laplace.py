import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft
from scipy.signal import square
from scipy.integrate import odeint

# Fourier Series
def square_wave_fourier_series(t, n_terms):
    result = 0
    for n in range(1, n_terms + 1, 2):
        term = (1/n) * np.sin(2 * np.pi * n * t)
        result += term
    return (4/np.pi) * result

# Fourier Transform
def plot_fft(t, signal, title):
    X = fft(signal)
    freqs = np.fft.fftfreq(len(t), t[1] - t[0])
    plt.plot(freqs, np.abs(X))
    plt.title(title)
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Magnitude")
    plt.xlim(0, 15)
    plt.grid()

# Laplace Transform - first-order system example
def first_order_system(y, t, K, tau):
    dydt = (-y + K) / tau
    return dydt

# Time domain
t = np.linspace(0, 2, 1000)
square_wave = square(2 * np.pi * t)

# Fourier series example
n_terms = 10
square_wave_approx = square_wave_fourier_series(t, n_terms)

# Fourier transform example
plot_fft(t, square_wave, "Fourier Transform of a Square Wave")

# Laplace transform example - first-order system response
K = 1
tau = 0.5
response = odeint(first_order_system, 0, t, args=(K, tau))

# Plot results
fig, axs = plt.subplots(3, 1, figsize=(8, 12))
axs[0].plot(t, square_wave, label="Square Wave")
axs[0].plot(t, square_wave_approx, label=f"Fourier Series ({n_terms} terms)")
axs[0].set_title("Fourier Series")
axs[0].set_xlabel("Time [s]")
axs[0].set_ylabel("Amplitude")
axs[0].legend()
axs[0].grid()

axs[1].plot(t, square_wave, label="Square Wave")
plot_fft(t, square_wave, "Fourier Transform of a Square Wave")
axs[1].set_title("Fourier Transform")
axs[1].set_xlabel("Frequency [Hz]")
axs[1].set_ylabel("Magnitude")
axs[1].set_xlim(0, 15)
axs[1].grid()

axs[2].plot(t, response, label="First-order System Response")
axs[2].set_title("Laplace Transform (First-order System Example)")
axs[2].set_xlabel("Time [s]")
axs[2].set_ylabel("Amplitude")
axs[2].legend()
axs[2].grid()

plt.tight_layout()
plt.show()