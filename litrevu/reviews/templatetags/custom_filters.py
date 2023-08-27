from django import template


register = template.Library()


@register.filter
def list_range(item):
    """Return a range of x number"""
    return range(int(item))
