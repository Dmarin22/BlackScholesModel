import numpy as np
import matplotlib.pyplot as plt
import math
import io
import base64
from scipy.stats import norm

# Helper functions to calculate d1 and d2
def d1(S, K, T, r, vol):
    return (math.log(S / K) + (r + 0.5 * vol ** 2) * T) / (vol * math.sqrt(T))

def d2(S, K, T, r, vol):
    return d1(S, K, T, r, vol) - (vol * math.sqrt(T))

# Greek calculation functions
def delta(S, K, T, r, vol, option_type="call"):
    d_1 = d1(S, K, T, r, vol)
    if option_type == "call":
        return norm.cdf(d_1)
    else:
        return norm.cdf(d_1) - 1

def gamma(S, K, T, r, vol):
    d_1 = d1(S, K, T, r, vol)
    return norm.pdf(d_1) / (S * vol * math.sqrt(T))

def vega(S, K, T, r, vol):
    d_1 = d1(S, K, T, r, vol)
    return S * norm.pdf(d_1) * math.sqrt(T)

def theta(S, K, T, r, vol, option_type="call"):
    d_1 = d1(S, K, T, r, vol)
    d_2 = d2(S, K, T, r, vol)
    first_term = -(S * norm.pdf(d_1) * vol) / (2 * math.sqrt(T))
    if option_type == "call":
        return first_term - r * K * math.exp(-r * T) * norm.cdf(d_2)
    else:
        return first_term + r * K * math.exp(-r * T) * norm.cdf(-d_2)

def rho(S, K, T, r, vol, option_type="call"):
    d_2 = d2(S, K, T, r, vol)
    if option_type == "call":
        return K * T * math.exp(-r * T) * norm.cdf(d_2)
    else:
        return -K * T * math.exp(-r * T) * norm.cdf(-d_2)

# Function to generate option price graph
def generate_option_price_graph(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):
    S_range = np.linspace(20, 60, 100)
    call_prices = []
    put_prices = []

    for S_current in S_range:
        d_1 = d1(S_current, strike_price, time_to_maturity, risk_free_rate, volatility)
        d_2 = d2(S_current, strike_price, time_to_maturity, risk_free_rate, volatility)
        call_prices.append(S_current * norm.cdf(d_1) - strike_price * math.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d_2))
        put_prices.append(strike_price * math.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d_2) - S_current * norm.cdf(-d_1))

    # Plot option prices
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, call_prices, label='Call Option Price', color='blue')
    plt.plot(S_range, put_prices, label='Put Option Price', color='red')
    plt.title('Black-Scholes Option Pricing Model')
    plt.xlabel('Underlying Price (S)')
    plt.ylabel('Option Price')
    plt.legend()
    plt.grid(True)

    # Encode plot to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64

# Function to generate Greek graphs and return them as base64 encoded images
def generate_greeks_graphs(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type="call"):
    S_range = np.linspace(20, 60, 100)
    delta_values = [delta(S, strike_price, time_to_maturity, risk_free_rate, volatility, option_type) for S in S_range]
    gamma_values = [gamma(S, strike_price, time_to_maturity, risk_free_rate, volatility) for S in S_range]

    greeks_images = {}

    # Delta Graph
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, delta_values, label="Delta", color='blue')
    plt.title("Delta vs Underlying Price")
    plt.xlabel("Underlying Price (S)")
    plt.ylabel("Delta")
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    greeks_images['delta'] = base64.b64encode(buf.read()).decode('utf-8')

    # Gamma Graph
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, gamma_values, label="Gamma", color='orange')
    plt.title("Gamma vs Underlying Price")
    plt.xlabel("Underlying Price (S)")
    plt.ylabel("Gamma")
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    greeks_images['gamma'] = base64.b64encode(buf.read()).decode('utf-8')

    return greeks_images
