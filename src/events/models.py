from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import timezone
import uuid

# Create your models here.
class Event(models.Model):
    id          =   models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        =   models.CharField(max_length=200)
    logo        =   models.CharField(max_length=200)
    img         =   models.CharField(max_length=200)
    description =   models.TextField()
    start_date  =   models.DateTimeField()
    end_date    =   models.DateTimeField()
    password    =   models.CharField(max_length=200, blank=True)
    slug        =   models.SlugField(max_length=55)
    def __str__(self):
        return self.name

class Scores(models.Model):
    user                    =   models.ForeignKey(User, on_delete=models.CASCADE)
    event                   =   models.ForeignKey(Event, on_delete=models.CASCADE)
    score                   =   models.PositiveIntegerField(default=0, db_index=True)
    last_submission_date    =   models.DateTimeField('Last Submission Date', default=timezone.now)
    class Meta:
        ordering = ['-score', 'last_submission_date', 'user__username']