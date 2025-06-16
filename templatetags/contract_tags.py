from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """Split the value by the argument"""
    return value.split(arg)

@register.filter
def strip(value):
    """Strip whitespace from the value"""
    return value.strip() if value else value 