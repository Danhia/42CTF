from django import template

register = template.Library()

@register.filter
def keyvalue(dict, key):    
    return dict[key]

@register.filter
def timestamp_fromdate(date):
    return str(date.timestamp() * 1000).replace(',','.')