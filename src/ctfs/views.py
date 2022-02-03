from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.models import timezone
from .models import Category, CTF, CTF_flags
from .forms import submit_flag
from accounts.models import UserProfileInfo
from django.utils.translation import get_language
from math import log
from accounts.models import UserProfileInfo

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
    if ctf.category.name == "-Intro-":
        return
    solves =  CTF_flags.objects.filter(ctf=ctf)
    nb_solves = len(solves)

    new_points = 200 - int(log(nb_solves)*8.5)*5

    if new_points != ctf.points:
        diff = ctf.points - new_points
        ctf.points = new_points
        ctf.save()
        for s in solves:
            s.user.userprofileinfo.score -= diff
            s.user.userprofileinfo.save()
        

def category(request, cat_slug):
    cat         =   get_object_or_404(Category, slug=cat_slug)
    ctfs        =   CTF.objects.filter(category=cat, event=None, disabled=False).order_by('points')
    for ex in ctfs:
        ex.solved_num   = CTF_flags.objects.filter(ctf=ex).count()
        ex.solved       = ex.solved_by(request.user)
    return render(request, 'ctfs/ctfs_list.html', {'ctfs' : ctfs, 'cat' : cat})

def ctf(request, cat_slug, ctf_slug):
    ctf_info    =   get_object_or_404(CTF, slug=ctf_slug, event=None)
    flagged     =   False
    solved_list =   CTF_flags.objects.filter(ctf=ctf_info).order_by('flag_date')
    description = get_description_by_lang(ctf_info)
    if request.user.is_authenticated:
        if CTF_flags.objects.filter(user=request.user, ctf=ctf_info):
            flagged = True
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = submit_flag(data=request.POST)
            if flagged == False and form.is_valid():
                if CTF.objects.filter(flag=request.POST.get('flag'), slug=ctf_slug, event=None):
                    new =   CTF_flags(user = request.user, ctf = ctf_info, flag_date = timezone.now())
                    new.save()
                    profil = UserProfileInfo.objects.get(user=request.user)
                    profil.last_submission_date = timezone.now()
                    profil.score += ctf_info.points
                    profil.save()
                    actualize_points(ctf_info)
                    return render(request, 'ctfs/ctf_info.html', { 'ctf' : ctf_info, 'solved_list': solved_list, 'valitated': True, 'description': description, 'date': timezone.now()})
                else:
                    return render(request, 'ctfs/ctf_info.html', { 'ctf' : ctf_info, 'solved_list': solved_list, 'failed': True, 'description': description, 'date': timezone.now()})
            else:
                return render(request, 'ctfs/ctf_info.html', { 'ctf' : ctf_info, 'solved_list': solved_list, 'alvalitated': True, 'description': description, 'date': timezone.now()})
        else:
            return render(request, 'ctfs/ctf_info.html', { 'ctf' : ctf_info, 'solved_list': solved_list, 'description': description, 'date': timezone.now()})
    else:
        return render(request, 'ctfs/ctf_info.html', { 'ctf' : ctf_info, 'solved_list': solved_list, 'alvalitated': flagged, 'description': description, 'date': timezone.now()})
