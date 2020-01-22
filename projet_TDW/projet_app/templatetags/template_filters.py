from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

FIRST_LIMIT = 75

@register.filter
@stringfilter
def beginning(string):
    return string[:FIRST_LIMIT]

def end(string):
    return string[FIRST_LIMIT:]

register.filter('start', beginning)
register.filter('end', end)

