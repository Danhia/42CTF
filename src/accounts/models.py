from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import timezone
from django.db.models import F, Min, Max
from secrets import token_hex

# Create your models here
class UserProfileInfo(models.Model):
    user                    =   models.OneToOneField(auth_models.User, on_delete=models.CASCADE)
    portfolio_site          =   models.URLField(blank=True)
    score                   =   models.PositiveIntegerField(default=0, db_index=True)
    last_submission_date    =   models.DateTimeField('Last Submission Date', default=timezone.now)
    token                   =   models.CharField(max_length=200, blank=True)
    discord_id              =   models.CharField(max_length=20, null=True, blank=True, unique=True)
    member                  =   models.BooleanField(default=False)
    member_since            =   models.DateTimeField('Member since', default=timezone.now)
    member_until            =   models.DateTimeField('Member until', default=timezone.now)
    def __str__(self):
        return self.user.username
    class Meta:
        ordering = ['-score', 'last_submission_date', 'user__username']
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'
        permissions = (("view_info", "View user info"),)

# Create your models here.
