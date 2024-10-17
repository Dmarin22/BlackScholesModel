from django.shortcuts import render
from .forms import OptionForm
from .utils import black_scholes
from .models import OptionCalculation

def calculate_option(request):
    option_price = None
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            stock_price = form.cleaned_data['stock_price']
            strike_price = form.cleaned_data['strike_price']
            time_to_maturity = form.cleaned_data['time_to_maturity']
            risk_free_rate = form.cleaned_data['risk_free_rate'] / 100  # Convert to decimal
            volatility = form.cleaned_data['volatility'] / 100  # Convert to decimal
            option_type = form.cleaned_data['option_type']

            # Calculate option price using the alternative Black-Scholes formula
            option_price = black_scholes(
                stock_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type
            )

            # Save the result to the database
            OptionCalculation.objects.create(
                stock_price=stock_price,
                strike_price=strike_price,
                time_to_maturity=time_to_maturity,
                risk_free_rate=risk_free_rate,
                volatility=volatility,
                option_type=option_type,
                option_price=option_price
            )
    else:
        form = OptionForm()

    return render(request, 'calculate_option.html', {'form': form, 'option_price': option_price})


