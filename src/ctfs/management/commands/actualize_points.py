from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from accounts.models import UserProfileInfo
from ctfs.models import CTF_flags, CTF
from math import log

class Command(BaseCommand):
    help = 'Actualize challenges points based on number of solves'

    def handle(self, *args, **options):
        challenges = CTF.objects.filter(event=None, disabled=False).exclude(category__name="-Intro-")
     
        for ctf in challenges:
            solves =  CTF_flags.objects.filter(ctf=ctf)
            nb_solves = len(solves)

            if nb_solves > 0:
                new_points = max(200 - int(log(nb_solves)*8.5)*5, 5)
            else:
                new_points = 200

            if new_points != ctf.points:
                diff = ctf.points - new_points
                ctf.points = new_points
                ctf.save()
                for s in solves:
                    s.user.userprofileinfo.score -= diff
                    s.user.userprofileinfo.save()