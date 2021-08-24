from django import template

register = template.Library()


@register.filter(name='split')
def split(value, key):
  return value.split(key)


@register.filter(name='zip1')
def zip1(a, b):
  return zip(a, b)


@register.filter
def get_type(value):
  return type(value)
