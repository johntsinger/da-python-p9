from django import template


register = template.Library()


@register.filter
def list_range(value):
    """Return a range of x number"""
    return range(int(value))
