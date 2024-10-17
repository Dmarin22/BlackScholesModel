from django.db import models

class OptionCalculation(models.Model):
    OPTION_TYPE_CHOICES = [
        ('call', 'Call'),
        ('put', 'Put'),
    ]

    stock_price = models.FloatField()
    strike_price = models.FloatField()
    time_to_maturity = models.FloatField(help_text="Time to maturity in years")
    risk_free_rate = models.FloatField(help_text="Risk-free rate as percentage")
    volatility = models.FloatField(help_text="Volatility as percentage")
    option_type = models.CharField(max_length=4, choices=OPTION_TYPE_CHOICES)
    option_price = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Option ({self.option_type.upper()}) - Price: {self.option_price:.2f}"

