from django import template

register = template.Library()

@register.filter
def format_currency(value):
    try:
        value = int(value) 
        return f"{value:,.0f}đ".replace(",", ".")  
    except (ValueError, TypeError):
        return value 
    
@register.filter(name='format_phone')
def format_phone(value):
    """Format phone number to (+84) XXX XXX XXX"""
    if len(value) == 10 and value.startswith('0'):
        return "(+84) {} {} {}".format(value[1:4], value[4:7], value[7:])
    return value

@register.filter(name='plus')
def plus(value, arg):
    """
    Adds the 'arg' to the value.
    """
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return value