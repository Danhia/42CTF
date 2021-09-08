from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from django import forms
from ctfs.models import Category, CTF_flags, CTF
from ..forms import UserForm,UserProfileInfoForm, UserInfosUpdateForm, UserUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse

from secrets import token_hex
from accounts.models import UserProfileInfo

from . import connection

def signin(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(username=username, password=password)
			if user:
				if user.is_active:
					login(request,user)
					return HttpResponseRedirect(reverse('home'))
				else:
					return HttpResponse(_("Your account was inactive."))
			else:
				return render(request, 'accounts/login.html', {'error': True})
		else:
			return render(request, 'accounts/login.html', {})
	else:
		return HttpResponseRedirect(reverse('home'))

def signup(request):
	if not request.user.is_authenticated:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()
		registered = False
		if request.method == 'POST':
			pass1 = request.POST.get('password')
			if len(pass1) < 8:
				return render(request,'accounts/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered_failed':"The new password must be at least %d characters long." % 8})
			first_isalpha = pass1[0].isalpha()
			if not any(c.isdigit() for c in pass1) or not any(c.isalpha() for c in pass1):
				return render(request,'accounts/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered_failed':_("The password must contain at least one letter and at least one digit or punctuation character.")})
			if User.objects.filter(email=request.POST.get('email')).exists():
				return render(request,'accounts/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered_failed':_("A user with that email already exists.")})
			user_form = UserForm(data=request.POST)
			profile_form = UserProfileInfoForm(data=request.POST)
			if user_form.is_valid() and profile_form.is_valid():
				user = user_form.save()
				user.set_password(user.password)
				user.save()
				profile = profile_form.save(commit=False)
				profile.user = user
				profile.token = token_hex(16)
				profile.save()
				registered = True
			else:
				return render(request,'accounts/register.html', {'user_form':user_form, 'profile_form':profile_form, 'registered_failed':_("A user with that username already exists.")})
		return render(request,'accounts/register.html',
				{'user_form':user_form,
					'profile_form':profile_form,
					'registered':registered})
	else:
		return HttpResponseRedirect(reverse('home'))

@login_required
def out(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))

@login_required
def edit(request):
	if request.method == 'POST':
		umail = request.user.email
		uuser = request.user.username
		p_form = UserInfosUpdateForm(request.POST, instance=request.user.userprofileinfo)
		u_form = UserUpdateForm(request.POST, instance=request.user)
		error = None
		success = None
		if p_form.is_valid() and u_form.is_valid():
			pmail = u_form.cleaned_data['email']
			if pmail == umail:
				pass
			else:
				if User.objects.filter(email=pmail).exists():
					error = _("Email already taken.")
			puser = u_form.cleaned_data['username']
			if puser == uuser:
				pass
			else:
				if User.objects.filter(username=puser).exists():
					error = _("Username already taken.")
			if error is None:
				u_form.save()
				p_form.save()
				success = _("Updated.")
		request.user.username = uuser

		context={'p_form': p_form, 'u_form': u_form, 'error':error, 'success' : success}
		return render(request, 'accounts/edit.html', context)
	else:
		p_form = UserInfosUpdateForm(instance=request.user.userprofileinfo)
		u_form = UserUpdateForm(instance=request.user)
		context={'p_form': p_form, 'u_form': u_form, 'token': request.user.userprofileinfo.token}
		return render(request, 'accounts/edit.html',context )

@login_required
def profile(request, user_name):
	catsDatas = []

	user_obj = get_object_or_404(User, username=user_name)
	cats = Category.objects.all()
	pointDatas = {}

	for cat in cats:
		# prepare categories
		solved_count = CTF_flags.objects.filter(user=user_obj, ctf__category__name=cat.name).count()
		max_count = CTF.objects.filter(category__name=cat.name).count()
		# get datas
		somme = 0
		solved = CTF_flags.objects.filter(user=user_obj, ctf__category__name=cat.name).order_by('flag_date')
		pointDatas[cat.name] = []
		pointDatas[cat.name].append([user_obj.date_joined.timestamp() * 1000, 0])
		percent = (solved_count / max_count) * 100
		catsDatas.append([cat.name, solved_count, max_count, '{:.0f}'.format(percent)])
		for flag in solved:
			somme += flag.ctf.points
			pointDatas[cat.name].append([flag.flag_date.timestamp() * 1000, somme])

	solves = CTF_flags.objects.filter(user=user_obj).order_by('-flag_date')
	solved = []
	somme = 0
	solved.append([user_obj.date_joined.timestamp() * 1000, 0])
	for s in solves.reverse():
		somme += s.ctf.points
		solved.append([s.flag_date.timestamp() * 1000,somme])
	return render(request,'accounts/profile.html', {'user':user_obj, 'solves':solves,'solved':solved,'catsDatas': catsDatas, 'pointDatas': pointDatas})

def rank(request, token):
	all_users	  = UserProfileInfo.objects.filter(score__gt=0).select_related().order_by('-score', 'last_submission_date', 'user__username')

	rank = 1
	for elem in all_users:
		if elem.token == token:
			break
		rank += 1
	data = {"rank": rank}
	return JsonResponse(data)
