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

def get_content_by_lang(news):
    lang = get_language()
    ret = None
    if lang == "fr":
        ret = news.content
    elif lang == "en":
        ret = news.content_en
    elif lang == "de":
        ret = news.content_de
    elif lang == "ru":
        ret = news.content_ru
    return ret

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
    latest_ctfs =   CTF.objects.filter(event=None).order_by('-pub_date')[:5]
    top10       =   UserProfileInfo.objects.select_related().order_by('-score', 'last_submission_date', 'user__username')[:10]
    nb_flags    =   CTF_flags.objects.count()
    nb_users    =   UserProfileInfo.objects.count()
    return render(request, 'home/home.html', {'news' : news, 'ctfs' : latest_ctfs, 'top' : top10, 'flags' : nb_flags})

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
