import math
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    S: Stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free interest rate (as a decimal)
    sigma: Volatility (as a decimal)
    option_type: 'call' or 'put'
    """
    
    # Calculate d1 and d2 using the alternative formula
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - (sigma * math.sqrt(T))

    # Calculate price for call or put option
    if option_type == 'call':
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    return price


