from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..forms import TeamUpdateForm
from ..models import Event, EventPlayer, Team
from ctfs.models import CTF, CTF_flags, Category
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from ..utils import get_random_name
from random import randint

@login_required
def create_team(request, event_slug):
	ev			=   get_object_or_404(Event, slug=event_slug)
	if request.method == 'POST':
		if request.user.is_authenticated and ev.team_size > 1:
			if Team.objects.filter(name=request.POST.get('teamname'), event=ev).exists():
				return render(request, 'events/create_team.html', {'event' : ev, 'logged': True, 'wrongpwd': False, 'registered' : True, 'exist' : True})
			new = Team(name=request.POST.get('teamname'), password=request.POST.get('password'), event=ev)
			new.save()
			player = EventPlayer.objects.get(user=request.user, event=ev)
			player.team = new
			player.save()
		return redirect('events:event_info', event_slug=event_slug)
	else:
		return render(request, 'events/create_team.html', {'event' : ev, 'logged': True, 'wrongpwd': False, 'registered' : True, 'exist' : False})

@login_required
def join_team(request, event_slug):
	ev    		=   get_object_or_404(Event, slug=event_slug)
	if request.method == 'POST':
		if request.user.is_authenticated and ev.team_size > 1:
			try:
				team  =   Team.objects.get(name=request.POST.get('teamname'), event=ev)
			except:
				team = None
			if team is None:
				return render(request, 'events/join_team.html', {'event' : ev, 'logged': True, 'wrongpwd': True, 'registered' : True, 'notexist' : True})
			else:
				members = EventPlayer.objects.filter(team=team)
			if request.POST.get('password') != team.password:
				return render(request, 'events/join_team.html', {'event' : ev, 'logged': True, 'wrongpwd': True, 'registered' : True, 'notexist' : False})
			if members.count() >= ev.team_size:
				return render(request, 'events/join_team.html', {'event' : ev, 'logged': True, 'wrongpwd': False, 'registered' : True, 'notexist' : False, 'max' : True})
			else:
				player = EventPlayer.objects.get(user=request.user, event=ev)
				player.team = team
				player.save()
		return redirect('events:event_info', event_slug=event_slug)
	else:
		return render(request, 'events/join_team.html', {'event' : ev, 'logged': True, 'wrongpwd': False, 'registered' : True, 'notexist' : False})

@login_required
def team_info(request, name, event_slug):
	event_info		=   get_object_or_404(Event, slug=event_slug)
	team 			=	Team.objects.get(name=name, event=event_info)

	catsDatas = []
	
	players = EventPlayer.objects.filter(team=team, event=event_info)
	users = [p.user for p in players]
	all_teams = list(Team.objects.filter(event=event_info).order_by('-score', 'last_submission_date', 'name'))
	rank = all_teams.index(get_object_or_404(Team, id=team.id, event=event_info)) + 1
	all_cats = Category.objects.all()
	cats = [cat for cat in all_cats if CTF.objects.filter(category__name=cat.name, event=event_info)]
	pointDatas = {}

	for cat in cats:
		# prepare categories
		solved_count = 0
		solved = []
		max_count = CTF.objects.filter(category__name=cat.name, event=event_info).count()
		somme = 0
		pointDatas[cat.name] = [[event_info.start_date.timestamp()*1000, 0]]
		for user_obj in users:
			# get datas
			solved_count += CTF_flags.objects.filter(user=user_obj, ctf__event=event_info , ctf__category__name=cat.name).count()
			solved += CTF_flags.objects.filter(user=user_obj, ctf__category__name=cat.name, ctf__event=event_info).order_by('flag_date')
		percent = (solved_count / max_count) * 100
		catsDatas.append([cat.name, solved_count, max_count, '{:.0f}'.format(percent)])
		for flag in solved:
			somme += flag.ctf.points
			pointDatas[cat.name].append([flag.flag_date.timestamp() * 1000, somme])

	query = Q()
	for user_obj in users:
		query |= Q(user=user_obj)
	query &= Q(ctf__event=event_info)

	solves = CTF_flags.objects.filter(query).order_by('-flag_date')
	solved = []
	somme = 0
	solved.append([event_info.start_date.timestamp() * 1000, 0])
	for s in solves.reverse():
		somme += s.ctf.points
		solved.append([s.flag_date.timestamp() * 1000,somme])

	return render(request,'events/team.html', {'users':users, 'solves':solves,'solved':solved,'catsDatas': catsDatas, 'pointDatas': pointDatas,
		'rank': rank, 'team':team, 'score':somme, 'event':event_info, 'cats':cats})

@login_required
def manage_team(request, event_slug):
	event_info	=   get_object_or_404(Event, slug=event_slug)
	player		= 	EventPlayer.objects.get(user=request.user, event=event_info)
	if not player.team:
		return render(request, 'events/create_team.html', {'event' : event_info, 'logged': True, 'wrongpwd': False, 'registered' : True, 'notexist' : False})
	members		=	EventPlayer.objects.filter(team=player.team, event=event_info)

	if request.method == 'POST':
		tname = player.team.name
		p_form = TeamUpdateForm(request.POST, instance=player.team)
		error = None
		success = None
		if p_form.is_valid():
			pname = p_form.cleaned_data['name']
			if pname == tname:
				pass
			else:
				if Team.objects.filter(name=pname, event=event_info).exists():
					error = _("Name already taken.")
			ppassword = p_form.cleaned_data['password']
			if error is None:
				p_form.save()
				success = _("Updated.")

		context={'p_form': p_form, 'error':error, 'success' : success, 'player':player, 'members':members}
		return render(request, 'events/manage_team.html', context)
	else:
		p_form = TeamUpdateForm(instance=player.team)
		context={'p_form': p_form, 'player':player, 'members':members}
		return render(request, 'events/manage_team.html',context)


@login_required
def leave_team(request, event_slug):
	event_info	=   get_object_or_404(Event, slug=event_slug)
	player		= 	EventPlayer.objects.get(user=request.user, event=event_info)
	team		=	Team.objects.get(event=event_info, name=player.team.name)

	team.score -= player.score
	team.save()
	player.team = None
	solved = CTF_flags.objects.filter(user=player.user, ctf__event=event_info)
	player.score = 0
	solved.delete()
	player.save()

	members		=	EventPlayer.objects.filter(team=team, event=event_info)
	if members.count() == 0:
		team.delete()

	return redirect('events:event_info', event_slug=event_slug)

@login_required
def find_team(request, event_slug):
	event_info	=   get_object_or_404(Event, slug=event_slug)
	teams		=	Team.objects.filter(event=event_info, auto=True)
	team 		= 	None
	player		=	EventPlayer.objects.get(user=request.user, event=event_info)

	if event_info.auto_match == False:
		return redirect('events:event_info', event_slug=event_slug)
	for t in teams:
		if EventPlayer.objects.filter(team=t, event=event_info).count() < event_info.team_size:
			team = t
			break

	if team is None:
		teamname = get_random_name()
		while Team.objects.filter(name=teamname, event=event_info).exists():
			teamname = get_random_name()
		team = Team(name=teamname, password="".join([str(randint(0,10)) for _ in range(16)]), event=event_info, auto=True)
		team.save()
			
	player.team = team
	player.save()

	return redirect('events:event_info', event_slug=event_slug)

@login_required
def open_team(request, event_slug):
	event_info	=   get_object_or_404(Event, slug=event_slug)
	player		=	EventPlayer.objects.get(user=request.user, event=event_info)

	if not player.team:
		return render(request, 'events/create_team.html', {'event' : event_info, 'logged': True, 'wrongpwd': False, 'registered' : True, 'notexist' : False})
	
	player.team.auto = True
	player.team.save()
	return redirect('events:manage_team', event_slug=event_slug)

@login_required
def close_team(request, event_slug):
	event_info	=   get_object_or_404(Event, slug=event_slug)
	player		=	EventPlayer.objects.get(user=request.user, event=event_info)

	if not player.team:
		return render(request, 'events/create_team.html', {'event' : event_info, 'logged': True, 'wrongpwd': False, 'registered' : True, 'notexist' : False})
	
	player.team.auto = False
	player.team.save()
	return redirect('events:manage_team', event_slug=event_slug)