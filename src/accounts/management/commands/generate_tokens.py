from collections import defaultdict
from django.core.management.base import BaseCommand, CommandError
from accounts import models as acc_models
from secrets import token_hex
from hashlib import md5

class Command(BaseCommand):
    help = 'Generate a new token for every user'

    def handle(self, *args, **options):
        all_users = acc_models.UserProfileInfo.objects.select_related().all()
        for elem in all_users:
            rand_value = md5((elem.user.username + token_hex(16)).encode('utf-8')).hexdigest()
            elem.token = rand_value
            elem.save()
