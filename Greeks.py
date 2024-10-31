# I'll define separate functions for each of the Greeks (Delta, Gamma, Vega, Theta, Rho)
# that take the same inputs as your original Black-Scholes function.

import math
from scipy.stats import norm

# Black-Scholes inputs
S = 42  # Underlying Price
K = 40  # Strike Price
T = 0.5  # Time to Expiration (in years)
r = 0.1  # Risk-Free Rate
vol = 0.2  # Volatility

# Helper functions to calculate d1 and d2
def d1(S, K, T, r, vol):
    return (math.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * math.sqrt(T))

def d2(S, K, T, r, vol):
    return d1(S, K, T, r, vol) - (vol * math.sqrt(T))

# Greek calculations

# Delta (Δ): Measures sensitivity to the underlying asset's price.
# It's the rate of change of the option price with respect to the price of the underlying asset.
def delta(S, K, T, r, vol, option_type="call"):
    """Calculates Delta for a call or put option."""
    d_1 = d1(S, K, T, r, vol)
    if option_type == "call":
        return norm.cdf(d_1)
    else:  # put option
        return norm.cdf(d_1) - 1


# Gamma (Γ): Measures the rate of change of Delta with respect to the underlying asset’s price.
# This represents the curvature of the option’s price in relation to the underlying.
def gamma(S, K, T, r, vol):
    """Calculates Gamma for both call and put options."""
    d_1 = d1(S, K, T, r, vol)
    return norm.pdf(d_1) / (S * vol * math.sqrt(T))

# Vega (ν): Measures sensitivity to volatility. It shows how much the option price will change with a 1% change in volatility.
def vega(S, K, T, r, vol):
    """Calculates Vega for both call and put options."""
    d_1 = d1(S, K, T, r, vol)
    return S * norm.pdf(d_1) * math.sqrt(T)

# Theta (θ): Measures sensitivity to time, often referred to as the time decay of the option.
# This shows how much the option price decreases as time to expiration decreases.
def theta(S, K, T, r, vol, option_type="call"):
    """Calculates Theta for a call or put option."""
    d_1 = d1(S, K, T, r, vol)
    d_2 = d2(S, K, T, r, vol)
    first_term = -(S * norm.pdf(d_1) * vol) / (2 * math.sqrt(T))
    if option_type == "call":
        return first_term - r * K * math.exp(-r * T) * norm.cdf(d_2)
    else:  # put option
        return first_term + r * K * math.exp(-r * T) * norm.cdf(-d_2)
    
# Rho (ρ): Measures sensitivity to the risk-free interest rate.
# This Greek shows how much the option price will change with a 1% change in interest rates.
def rho(S, K, T, r, vol, option_type="call"):
    """Calculates Rho for a call or put option."""
    d_2 = d2(S, K, T, r, vol)
    if option_type == "call":
        return K * T * math.exp(-r * T) * norm.cdf(d_2)
    else:  # put option
        return -K * T * math.exp(-r * T) * norm.cdf(-d_2)

# Calculating each Greek for the given parameters
delta_call = delta(S, K, T, r, vol, "call")
delta_put = delta(S, K, T, r, vol, "put")
gamma_value = gamma(S, K, T, r, vol)
vega_value = vega(S, K, T, r, vol)
theta_call = theta(S, K, T, r, vol, "call")
theta_put = theta(S, K, T, r, vol, "put")
rho_call = rho(S, K, T, r, vol, "call")
rho_put = rho(S, K, T, r, vol, "put")

# Display the results
(delta_call, delta_put, gamma_value, vega_value, theta_call, theta_put, rho_call, rho_put)
