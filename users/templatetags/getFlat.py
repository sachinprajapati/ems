from django import template
from django.template.defaultfilters import stringfilter

from users.functions import *

register = template.Library()

@register.filter
@stringfilter
def getFlatDetail(value):
    return getFlatDetailByKey(value)