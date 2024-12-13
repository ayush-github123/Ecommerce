from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg

@register.filter(name='total_price')
def total_price(items):
    return sum(item.quantity * item.product.price for item in items)
