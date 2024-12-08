from django.shortcuts import render
from .forms import OptionForm
from .utils import black_scholes
from .models import OptionCalculation
from .graphs import generate_option_price_graph
def intro_page(request):
    """
    Renders the introductory page for the options simulator.
    """
    return render(request, 'intro.html')
def calculate_option(request):
    option_price = None
    graph = None
    intro = True  # Flag to indicate if this is the introductory page

    if request.method == 'POST':
        intro = False  # Switch to calculator functionality
        form = OptionForm(request.POST)
        if form.is_valid():
            stock_price = form.cleaned_data['stock_price']
            strike_price = form.cleaned_data['strike_price']
            time_to_maturity = form.cleaned_data['time_to_maturity']
            risk_free_rate = form.cleaned_data['risk_free_rate'] / 100  # Convert to decimal
            volatility = form.cleaned_data['volatility'] / 100  # Convert to decimal
            option_type = form.cleaned_data['option_type']

            # Calculate the option price
            option_price = black_scholes(
                stock_price, strike_price, time_to_maturity, risk_free_rate, volatility, option_type
            )

            # Save calculation to the database
            OptionCalculation.objects.create(
                stock_price=stock_price,
                strike_price=strike_price,
                time_to_maturity=time_to_maturity,
                risk_free_rate=risk_free_rate,
                volatility=volatility,
                option_type=option_type,
                option_price=option_price
            )

            # Generate the option price graph
            graph = generate_option_price_graph(stock_price, strike_price, time_to_maturity, risk_free_rate, volatility)
    else:
        form = OptionForm()

    return render(request, 'calculate_option.html', {
        'form': form,
        'option_price': option_price,
        'graph': graph,
        'intro.html': intro
    })
