from django import template

register = template.Library()

@register.filter
def index(src, arg):
    return src[arg]


@register.filter
def linebreaker(src):
    result = src.split('\n')
    return result[0]

@register.filter
def sub(src, arg):
    return src-arg

@register.filter
def num_range(src):
    return [x for x in range(1, src+1)]
