from django import template
from django.template.defaultfilters import stringfilter

from users.functions import *

register = template.Library()

@register.filter
@stringfilter
def getFlatDetail(value):
    return getFlatDetailByKey(value)

@stringfilter
@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def multiply(value, arg):
	print("value", value, type(value), arg, type(arg))
	return float(value)*float(arg)