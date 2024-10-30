import numpy as np
import matplotlib.pyplot as plt
import math
import io
import base64
from scipy.stats import norm

def generate_option_price_graph(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility):
    # Generate a range of underlying prices for plotting
    S_range = np.linspace(20, 60, 100)
    call_prices = []
    put_prices = []

    # Calculate call and put prices across a range of stock prices
    for S_current in S_range:
        d1 = (math.log(S_current / strike_price) + (risk_free_rate + 0.5 * volatility ** 2) * time_to_maturity) / (volatility * math.sqrt(time_to_maturity))
        d2 = d1 - volatility * math.sqrt(time_to_maturity)
        call_prices.append(S_current * norm.cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_maturity) * norm.cdf(d2))
        put_prices.append(strike_price * math.exp(-risk_free_rate * time_to_maturity) * norm.cdf(-d2) - S_current * norm.cdf(-d1))

    # Generate the plot
    plt.figure(figsize=(10, 6))
    plt.plot(S_range, call_prices, label='Call Option Price', color='blue')
    plt.plot(S_range, put_prices, label='Put Option Price', color='red')
    plt.title('Black-Scholes Option Pricing Model')
    plt.xlabel('Underlying Price (S)')
    plt.ylabel('Option Price')
    plt.legend()
    plt.grid(True)

    # Save plot to a PNG image in memory
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Encode image to display in HTML
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64
