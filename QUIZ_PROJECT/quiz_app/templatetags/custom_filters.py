from django import template

register = template.Library()

@register.filter
def contains(value, arg):
    """Check if arg is in a comma-separated string"""
    if not value:
        return False
    return arg in value.split(',')
