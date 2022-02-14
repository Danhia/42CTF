from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import timezone
from ..forms import submit_flag
from ..models import Event, EventPlayer, Team
from ctfs.models import CTF, CTF_flags, Category
from django.utils.translation import get_language
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from math import log

def get_description_by_lang(ctf):
	lang = get_language()
	ret = None
	if lang == "fr":
		ret = ctf.description
	elif lang == "en":
		ret = ctf.description_en
	elif lang == "de":
		ret = ctf.description_de
	elif lang == "ru":
		ret = ctf.description_ru
	return ret

def actualize_points(ctf):
	solves =  CTF_flags.objects.filter(ctf=ctf)
	nb_solves = len(solves)

	new_points = max(50 - int(log(nb_solves)*2.5)*5, 5)

	if new_points != ctf.points:
		diff = ctf.points - new_points
		ctf.points = new_points
		ctf.save()
		for s in solves:
			player = EventPlayer.objects.get(event=ctf.event, user=s.user)
			player.score -= diff
			player.save()
			if player.team:
				player.team.score -= diff
				player.team.save()

# Create your views here.
def events(request):
	list_events        =   Event.objects.filter().order_by('-end_date', 'start_date')
	return render(request, 'events/events_list.html', {'events' : list_events, 'curdate': timezone.now()})

def chall_event_info(request, event_slug, chall_slug):
	event_info  = get_object_or_404(Event, slug=event_slug)
	ctf_info    = get_object_or_404(CTF, event__slug=event_info.slug, slug=chall_slug)

	if timezone.now() < ctf_info.pub_date:
		return redirect('events:event_info', event_slug=event_slug)
	eventisover = False
	alreadyflag = False
	congrat     = False
	wrongflag   = False
	errorform   = False
	notsub      = False
	noteam		= False
	player		= None
	if request.user.is_authenticated and not request.user.is_staff:
		player = EventPlayer.objects.filter(event=event_info, user=request.user)
		if not player:
			return redirect('events:event_info', event_slug=event_slug)
	elif not request.user.is_authenticated:
		return redirect('accounts:signin')
	if request.GET.get('EventIsOver') or timezone.now() > event_info.end_date:
		eventisover = True
	if request.GET.get('AlreadyFlagged'):
		alreadyflag = True
	if request.GET.get('Congrat'):
		congrat     = True
	if request.GET.get('WrongFlag'):
		wrongflag   = True
	if request.GET.get('ErrorInForm'):
		errorform   = True
	if request.GET.get('NotRegistered'):
		notsub      = True
	if request.GET.get('NoTeam'):
		noteam      = True
	solved_challs = CTF_flags.objects.filter(ctf=ctf_info).order_by('flag_date')
	solved_list = []
	for s in solved_challs:
		if event_info.team_size > 1:
			solved_list.append([s.user, s.flag_date, EventPlayer.objects.get(event=event_info, user=s.user).team.name])
		else:
			solved_list.append([s.user, s.flag_date])
	description = get_description_by_lang(ctf_info)
	return render(request, 'events/ctf_info.html', { 'ctf' : ctf_info, 'event':event_info, 'solved_list': solved_list, 'description': description, 'eventisover': eventisover, 'alreadyflag': alreadyflag,
		'congrat': congrat, 'wrongflag': wrongflag, 'errorform': errorform, 'notsub': notsub, 'noteam':noteam})

def event(request, event_slug):
	event_info 			= get_object_or_404(Event, slug=event_slug)
	IsRegistered		= False
	wrongpwd			= False
	alreadyregistered	= False
	subisover			= False
	if request.GET.get('WrongPassword'):
		wrongpwd = True
	if request.GET.get('AlreadyRegistered'):
		alreadyregistered = True
	if request.GET.get('SubscriptionIsOver'):
		subisover = True
	if request.user.is_authenticated:
		try:
			player = EventPlayer.objects.get(event=event_info, user=request.user)
		except:
			player = None
		if player:
			IsRegistered = True
	if event_info.password:
		if request.user.is_authenticated:
			if request.user.is_staff is False:
				if not player:
					return render(request, 'events/event_pwd.html', {'event' : event_info, 'logged': True, 'wrongpwd': wrongpwd, 'alreadyregistered': alreadyregistered})
		else:
			return render(request, 'events/event_pwd.html', {'event' : event_info, 'logged': False, 'wrongpwd': wrongpwd, 'alreadyregistered': alreadyregistered})
	ended = False
	if timezone.now() >= event_info.end_date:
		ended = True
	begun = False
	if timezone.now() >= event_info.start_date:
		begun = True
	challenges  = CTF.objects.filter(event=event_info, pub_date__lte=timezone.now()).order_by('category', 'points')
	if event_info.team_size == 1:
		solved_list = EventPlayer.objects.filter(event=event_info).order_by('-score', 'last_submission_date', 'user__username')
	else:
		solved_list = Team.objects.filter(event=event_info).order_by('-score', 'last_submission_date', 'name')
	return render(request, 'events/event_info.html', {'event' : event_info, 'IsRegistered': IsRegistered, 'ctfs': challenges, 'solved_list':solved_list, 
		'ended': ended, 'begun': begun, 'wrongpwd': wrongpwd, 'alreadyregistered': alreadyregistered, 'subisover': subisover})

@login_required
def submit_event_flag(request, event_slug, chall_slug):
	ev          =   get_object_or_404(Event, slug=event_slug)
	response    =   redirect('events:event_chall_info', event_slug=event_slug, chall_slug=chall_slug)
	flagged     =   False

	if timezone.now() >= ev.end_date:
		response['Location'] += '?EventIsOver=1'
		return response

	if request.method == 'POST':
		ctf_info    =   CTF.objects.get(event=ev, slug=chall_slug)
		if not ctf_info:
			response['Location'] += '?ChallengeNotFound=1'
			return response
		
		try:
			player = EventPlayer.objects.get(event=ev, user=request.user)
		except:
			player = None
		
		if player:
			if ev.team_size > 1 and player.team is None:
					response['Location'] += '?NoTeam=1'
					return response
			if ev.team_size == 1 and CTF_flags.objects.filter(user=request.user, ctf=ctf_info):
				flagged = True
			else:
				solved_list = CTF_flags.objects.filter(ctf=ctf_info)
				for s in solved_list:
					tmp = EventPlayer.objects.get(user=s.user, event=ev)
					if tmp.team == player.team:
						flagged = True
			if flagged == True:
				response['Location'] += '?AlreadyFlagged=1'
				return response

			form = submit_flag(data=request.POST)

			if form.is_valid():
				if ctf_info.flag == request.POST.get('flag'):
					new =   CTF_flags(user = request.user, ctf = ctf_info, flag_date = timezone.now())
					new.save()
					if ctf_info.points > 0:
						player.last_submission_date = timezone.now()
					player.score += ctf_info.points
					player.save()
					if player.team:
						if ctf_info.points > 0:
							player.team.last_submission_date = timezone.now()
						player.team.score += ctf_info.points
						player.team.save()
					if ev.dynamic:
						actualize_points(ctf_info)
					response['Location'] += '?Congrat=1'
					return response
				else:
					response['Location'] += '?WrongFlag=1'
					return response
			else:
				response['Location'] += '?ErrorInForm=1'
				return response
		else:
			response['Location'] += '?NotRegistered=1'
			return response
	return response

@login_required
def submit_pwd(request, event_slug):
	response = redirect('events:event_info', event_slug=event_slug)
	event_info  = get_object_or_404(Event, slug=event_slug)
	if request.method == 'POST':
		if request.user.is_authenticated:
			ev    =   get_object_or_404(Event, slug=event_slug)
			if ev == False:
				response['Location'] += '?NoEventFound=1'
				return response

			if request.POST.get('password') != ev.password:
				response['Location'] += '?WrongPassword=1'
				return response

			if EventPlayer.objects.filter(user=request.user, event=ev).exists() or EventPlayer.objects.filter(user=request.user, event=ev).exists():
				response['Location'] += '?AlreadyRegistered=1'
				return response
			else:
				new = EventPlayer(user=request.user, event=ev)
				new.save()
	return redirect('events:event_info', event_slug=event_slug)
		

@login_required
def register_to_event(request, event_slug):
	response = redirect('events:event_info', event_slug=event_slug)
	if request.method == 'POST':
		if request.user.is_authenticated:
			ev    =   get_object_or_404(Event, slug=event_slug)
			if ev == False:
				response['Location'] += '?NoEventFound=1'
				return response
			if timezone.now() >= ev.end_date:
				response['Location'] += '?SubscriptionIsOver=1'
				return response
			if EventPlayer.objects.filter(user=request.user, event=ev).exists():
				response['Location'] += '?AlreadyRegistered=1'
				return response
			else:
				new = EventPlayer(user=request.user, event=ev, score=0)
				new.save()
	return redirect('events:event_info', event_slug=event_slug)

@login_required
def profile(request, user_name, event_slug):
	catsDatas = []

	event_info    =   get_object_or_404(Event, slug=event_slug)
	user_obj = get_object_or_404(User, username=user_name)
	player = EventPlayer.objects.get(user=user_obj, event=event_info)
	all_players = list(EventPlayer.objects.filter(event=event_info).order_by('-score', 'last_submission_date', 'user__username'))
	rank = all_players.index(get_object_or_404(EventPlayer, user=user_obj, event=event_info)) + 1
	all_cats = Category.objects.all()
	cats = [cat for cat in all_cats if CTF.objects.filter(category__name=cat.name, event=event_info)]
	pointDatas = {}

	for cat in cats:
		# prepare categories
		solved_count = CTF_flags.objects.filter(user=user_obj, ctf__event=event_info , ctf__category__name=cat.name).count()
		max_count = CTF.objects.filter(category__name=cat.name, event=event_info).count()
		# get datas
		somme = 0
		solved = CTF_flags.objects.filter(user=user_obj, ctf__category__name=cat.name, ctf__event=event_info).order_by('flag_date')
		pointDatas[cat.name] = []
		pointDatas[cat.name].append([event_info.start_date.timestamp() * 1000, 0])
		percent = (solved_count / max_count) * 100
		catsDatas.append([cat.name, solved_count, max_count, '{:.0f}'.format(percent)])
		for flag in solved:
			somme += flag.ctf.points
			pointDatas[cat.name].append([flag.flag_date.timestamp() * 1000, somme])

	solves = CTF_flags.objects.filter(user=user_obj, ctf__event=event_info).order_by('-flag_date')
	solved = []
	somme = 0
	solved.append([event_info.start_date.timestamp() * 1000, 0])
	for s in solves.reverse():
		somme += s.ctf.points
		solved.append([s.flag_date.timestamp() * 1000,somme])

	return render(request,'accounts/profile.html', {'user':user_obj, 'solves':solves,'solved':solved,'catsDatas': catsDatas, 'pointDatas': pointDatas,
		'rank': rank, 'score' : somme, 'cats':cats})


