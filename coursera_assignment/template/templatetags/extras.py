from django import template

register = template.Library()


@register.filter(name='inc')
def inc(value, inc_value):
    return value + inc_value


@register.inclusion_tag(name='division')
def division(a, b, to_int=False):
    if to_int:
        return int(int(a) / int(b))
    else:
        return float(a) / float(b)