from django import template


register = template.Library()


@register.simple_tag
@register.filter()
def mediapath(val):
    if val:
        return val.url
    return '#'

