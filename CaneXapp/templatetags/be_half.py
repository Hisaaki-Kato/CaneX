from django import template

register = template.Library()

@register.filter
def be_half(value):
    return (value / 2)