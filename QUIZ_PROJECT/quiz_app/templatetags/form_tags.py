# quiz_app/templatetags/form_tags.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    try:
        return field.as_widget(attrs={"class": css})
    except AttributeError:
        # If it's not a form field, just return as-is
        return field
