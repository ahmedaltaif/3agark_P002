from django import template
from django.template.defaultfilters import floatformat

register = template.Library()

@register.filter
def format_number(value):
    """Format a number with commas for thousands separator"""
    try:
        if value is None:
            return "0"
        # Convert to float and format with commas
        value = float(value)
        if value.is_integer():
            # If it's a whole number, format without decimal places
            return "{:,.0f}".format(value)
        else:
            # If it has decimal places, format with 2 decimal places
            return "{:,.2f}".format(value)
    except (ValueError, TypeError):
        return value 