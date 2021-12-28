from django import template
from ctfs.models import CTF_flags
from events.models import EventPlayer

register = template.Library()

@register.simple_tag
def isflagged(user, ctf):
	flagged		= False
	event_info	= ctf.event

	if event_info.team_size == 1:
		if CTF_flags.objects.filter(user=user, ctf=ctf):
			flagged = True
	elif EventPlayer.objects.filter(user=user, event=event_info):
		player = EventPlayer.objects.get(user=user, event=event_info)
		solved_list = CTF_flags.objects.filter(ctf=ctf)
		for s in solved_list:
			tmp = EventPlayer.objects.get(user=s.user, event=event_info)
			if tmp.team == player.team:
				flagged = True

	if flagged:
		return "success-msg"
	return ""