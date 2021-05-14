from django import template

register = template.Library()


@register.filter
def add_symbol(value, arg='#'):
    return str(arg) + str(value)


@register.filter(name='times')
def times(number):
    return range(number)
