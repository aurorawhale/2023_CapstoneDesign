from django import template

register = template.Library()

@register.filter
def index(src, arg):
    return src[arg]
