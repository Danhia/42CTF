from django import template
from ctfs.models import CTF_flags

register = template.Library()

@register.simple_tag
def isflagged(user, ctf):
    if CTF_flags.objects.filter(user=user, ctf=ctf):
        return "success-msg"
    return ""
