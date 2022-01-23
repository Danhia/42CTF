from django import template
from django.contrib.auth.models import timezone

register = template.Library()

@register.simple_tag
def ismember(user):
	if user.member and user.member_until > timezone.now():
		return "is-member"
	return ""