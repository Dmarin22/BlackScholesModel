from django import forms

class OptionForm(forms.Form):
    stock_price = forms.FloatField(label="Stock Price")
    strike_price = forms.FloatField(label="Strike Price")
    time_to_maturity = forms.FloatField(label="Time to Maturity (years)")
    risk_free_rate = forms.FloatField(label="Risk-Free Rate (%)")
    volatility = forms.FloatField(label="Volatility (%)")
    option_type = forms.ChoiceField(choices=[('call', 'Call'), ('put', 'Put')], label="Option Type")
