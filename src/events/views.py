from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import timezone
from .forms import submit_flag
from .models import Event, Scores
from ctfs.models import CTF, CTF_flags
from django.utils.translation import get_language

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

# Create your views here.
def events(request):
    list_events        =   Event.objects.filter().order_by('-end_date', 'start_date')
    return render(request, 'events/events_list.html', {'events' : list_events, 'curdate': timezone.now()})

def chall_event_info(request, event_slug, chall_slug):
    event_info  = get_object_or_404(Event, slug=event_slug)
    ctf_info    = get_object_or_404(CTF, event__slug=event_info.slug, slug=chall_slug)
    if request.user.is_authenticated and not request.user.is_staff:
        userScore = Scores.objects.filter(event=event_info, user=request.user)
        if not userScore:
            return redirect('/')
    solved_list = CTF_flags.objects.filter(ctf=ctf_info).order_by('flag_date')
    description = get_description_by_lang(ctf_info)
    return render(request, 'events/ctf_info.html', { 'ctf' : ctf_info, 'event':event_info, 'solved_list': solved_list, 'description': description})

def event(request, event_slug):
    event_info  = get_object_or_404(Event, slug=event_slug)
    IsRegistered = False
    if request.user.is_authenticated:
        userScore = Scores.objects.filter(event=event_info, user=request.user)
        if userScore:
            IsRegistered = True
    if event_info.password:
        if request.user.is_authenticated:
            if request.user.is_staff is False:
                if not userScore:
                    return render(request, 'events/event_pwd.html', {'event' : event_info, 'logged': True})
        else:
            return render(request, 'events/event_pwd.html', {'event' : event_info, 'logged': False})
    ended = False
    if timezone.now() >= event_info.end_date:
        ended = True
    begun = False
    if timezone.now() >= event_info.start_date:
        begun = True
    challenges  = CTF.objects.filter(event=event_info).order_by('category', 'points')
    solved_list = Scores.objects.filter(event=event_info).order_by('-score', 'last_submission_date', 'user__username')
    return render(request, 'events/event_info.html', {'event' : event_info, 'IsRegistered': IsRegistered, 'ctfs': challenges, 'solved_list':solved_list, 'ended': ended, 'begun': begun})

@login_required
def submit_event_flag(request, event_slug, chall_slug):
    ev          =   get_object_or_404(Event, slug=event_slug)
    response    =   redirect('events:event_chall_info', event_slug=event_slug, chall_slug=chall_slug)
    if timezone.now() >= ev.end_date:
        response['Location'] += '?EventIsOver'
        return response

    if request.method == 'POST':
        ctf_info    =   CTF.objects.get(event=ev, slug=chall_slug)
        if not ctf_info:
            response['Location'] += '?ChallengeNotFound'
            return response
        flagged     =   False
        if CTF_flags.objects.filter(user=request.user, ctf=ctf_info):
            flagged = True
            response['Location'] += '?AlreadyFlagged'
            return response
        try:
            score = Scores.objects.get(user=request.user, event=ev)
        except:
            score = None
        if score:
            form = submit_flag(data=request.POST)
            if flagged == False and form.is_valid():
                if ctf_info.flag == request.POST.get('flag'):
                    new =   CTF_flags(user = request.user, ctf = ctf_info, flag_date = timezone.now())
                    new.save()
                    score.last_submission_date = timezone.now()
                    score.score += ctf_info.points
                    score.save()
                    response['Location'] += '?Congrat'
                    return response
                else:
                    response['Location'] += '?WrongFlag'
                    return response
            else:
                response['Location'] += '?ErrorInForm'
                return response
    return response

@login_required
def submit_pwd(request, event_slug):
    response = redirect('events:event_info', event_slug=event_slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            ev    =   get_object_or_404(Event, slug=event_slug)
            if ev == False:
                response['Location'] += '?NoEventFound'
                return response

            if request.POST.get('password') != ev.password:
                response['Location'] += '?WrongPassword'
                return response

            if Scores.objects.filter(user=request.user, event=ev).exists():
                response['Location'] += '?AlreadyRegistered'
                return response
            else:
                new = Scores(user=request.user, event=ev, score=0)
                new.save()
    return redirect('events:event_info', event_slug=event_slug)

@login_required
def subscribe_to_event(request, event_slug):
    response = redirect('events:event_info', event_slug=event_slug)
    if request.method == 'POST':
        if request.user.is_authenticated:
            ev    =   get_object_or_404(Event, slug=event_slug)
            if ev == False:
                response['Location'] += '?NoEventFound'
                return response
            if timezone.now() >= ev.end_date:
                response['Location'] += '?SubscriptionIsOver'
                return response
            if Scores.objects.filter(user=request.user, event=ev).exists():
                response['Location'] += '?AlreadyRegistered'
                return response
            else:
                new = Scores(user=request.user, event=ev, score=0)
                new.save()
    return redirect('events:event_info', event_slug=event_slug)
