import math
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

# Redefining the Greek calculation functions

# Helper functions to calculate d1 and d2
def d1(S, K, T, r, vol):
    return (math.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * math.sqrt(T))

def d2(S, K, T, r, vol):
    return d1(S, K, T, r, vol) - (vol * math.sqrt(T))

# Delta
def delta(S, K, T, r, vol, option_type="call"):
    d_1 = d1(S, K, T, r, vol)
    if option_type == "call":
        return norm.cdf(d_1)
    else:  # put option
        return norm.cdf(d_1) - 1

# Gamma
def gamma(S, K, T, r, vol):
    d_1 = d1(S, K, T, r, vol)
    return norm.pdf(d_1) / (S * vol * math.sqrt(T))

# Vega
def vega(S, K, T, r, vol):
    d_1 = d1(S, K, T, r, vol)
    return S * norm.pdf(d_1) * math.sqrt(T)

# Theta
def theta(S, K, T, r, vol, option_type="call"):
    d_1 = d1(S, K, T, r, vol)
    d_2 = d2(S, K, T, r, vol)
    first_term = -(S * norm.pdf(d_1) * vol) / (2 * math.sqrt(T))
    if option_type == "call":
        return first_term - r * K * math.exp(-r * T) * norm.cdf(d_2)
    else:  # put option
        return first_term + r * K * math.exp(-r * T) * norm.cdf(-d_2)

# Rho
def rho(S, K, T, r, vol, option_type="call"):
    d_2 = d2(S, K, T, r, vol)
    if option_type == "call":
        return K * T * math.exp(-r * T) * norm.cdf(d_2)
    else:  # put option
        return -K * T * math.exp(-r * T) * norm.cdf(-d_2)

# Parameters for the plot
S_range = np.linspace(20, 80, 100)  # Range of underlying prices for the plot
K = 40  # Strike Price
T = 0.5  # Time to Expiration (in years)
r = 0.1  # Risk-Free Rate
vol = 0.2  # Volatility

# Calculate Greeks for each underlying price in S_range
delta_values = [delta(S, K, T, r, vol, "call") for S in S_range]
gamma_values = [gamma(S, K, T, r, vol) for S in S_range]
vega_values = [vega(S, K, T, r, vol) for S in S_range]
theta_values = [theta(S, K, T, r, vol, "call") for S in S_range]
rho_values = [rho(S, K, T, r, vol, "call") for S in S_range]

# Plotting each Greek
plt.figure(figsize=(14, 10))

# Delta
plt.subplot(3, 2, 1)
plt.plot(S_range, delta_values, label="Delta", color='blue')
plt.title("Delta vs Underlying Price")
plt.xlabel("Underlying Price (S)")
plt.ylabel("Delta")
plt.grid(True)

# Gamma
plt.subplot(3, 2, 2)
plt.plot(S_range, gamma_values, label="Gamma", color='orange')
plt.title("Gamma vs Underlying Price")
plt.xlabel("Underlying Price (S)")
plt.ylabel("Gamma")
plt.grid(True)

# Vega
plt.subplot(3, 2, 3)
plt.plot(S_range, vega_values, label="Vega", color='green')
plt.title("Vega vs Underlying Price")
plt.xlabel("Underlying Price (S)")
plt.ylabel("Vega")
plt.grid(True)

# Theta
plt.subplot(3, 2, 4)
plt.plot(S_range, theta_values, label="Theta", color='red')
plt.title("Theta vs Underlying Price")
plt.xlabel("Underlying Price (S)")
plt.ylabel("Theta")
plt.grid(True)

# Rho
plt.subplot(3, 2, 5)
plt.plot(S_range, rho_values, label="Rho", color='purple')
plt.title("Rho vs Underlying Price")
plt.xlabel("Underlying Price (S)")
plt.ylabel("Rho")
plt.grid(True)

# Adjust layout
plt.tight_layout()
plt.show()
