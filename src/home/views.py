from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from .models import new
from ctfs.models import Category, CTF, CTF_flags
from accounts.models import UserProfileInfo
from django.urls import translate_url
from django.utils.translation import (
    LANGUAGE_SESSION_KEY, check_for_language, get_language,
)
from django.core.files.storage import default_storage
import datetime
from collections import defaultdict
import operator

def get_weekly_top():
    week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    weekly_flags = CTF_flags.objects.filter(flag_date__gt=week_ago, ctf__disabled=False, ctf__event=None)
    scores = defaultdict(int)

    for sol in weekly_flags:
            scores[sol.user] += sol.ctf.points

    users = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    users = [(u[0].userprofileinfo, u[1]) for u in users]

    return(users[:5])

def home(request):
    lang_code = get_language()
    if hasattr(request, 'session') and LANGUAGE_SESSION_KEY in request.session:
        lang_code = request.session[LANGUAGE_SESSION_KEY]
    url_translated = translate_url(request.path, lang_code)
    if request.path != url_translated:
        print("%s\n%s" % (request.path, url_translated))
        response = HttpResponseRedirect(url_translated)
        return response
    news        =   new.objects.order_by('-pub_date')[:5]
    latest_ctfs =   CTF.objects.filter(event=None, disabled=False).order_by('-pub_date')[:5]
    top10       =   UserProfileInfo.objects.select_related().order_by('-score', 'last_submission_date', 'user__username')[:10]
    nb_flags    =   CTF_flags.objects.count()
    nb_users    =   UserProfileInfo.objects.count()
    latest_flags = CTF_flags.objects.filter(ctf__event = None, ctf__disabled=False).order_by('-flag_date')[:5]
    top_weekly = get_weekly_top()

    return render(request, 'home/home.html', {'news' : news, 'ctfs' : latest_ctfs, 'top' : top10, 'flags' : nb_flags, 
    'latest_flags':latest_flags, 'top_weekly': top_weekly, 'nb_users': nb_users})

def cgu(request):
    return render(request, 'cgu.html')


def set_language(request, lang_code):
    next = '/'
    if request.GET.get('next'):
        next = request.GET.get('next')
    response = HttpResponseRedirect(next)
    if lang_code and check_for_language(lang_code):
        if next:
            next_trans = translate_url(next, lang_code)
            if next_trans != next:
                response = HttpResponseRedirect(next_trans)
        if hasattr(request, 'session'):
            request.session[LANGUAGE_SESSION_KEY] = lang_code
        else:
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                )
        return redirect('/'+lang_code+next)


# Create your views here.
