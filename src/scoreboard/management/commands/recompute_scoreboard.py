from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from accounts.models import UserProfileInfo
from ctfs import models as ex_models

class Command(BaseCommand):
    help = 'Recomputes the score cache from the solutions'

    def handle(self, *args, **options):
        all_sols = ex_models.CTF_flags.objects.select_related().filter(ctf__event=None, ctf__disabled=False)
        all_users = UserProfileInfo.objects.all()
     
        scores = defaultdict(int)
        for sol in all_sols:
            scores[sol.user] += sol.ctf.points

        for u in all_users:
            if u.user not in scores.keys():
                u.score = 0
                u.save()

        for u in scores:
            u.userprofileinfo.score = scores[u]
            u.userprofileinfo.save()
