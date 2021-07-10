from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name        =   models.CharField(max_length=200)
    description =   models.TextField()
    slug        =   models.SlugField(max_length=55)
    def __str__(self):
        return self.name

class CTF(models.Model):
    name        =   models.CharField(max_length=200)
    flag        =   models.CharField(max_length=100)
    description =   models.TextField(blank=True)
    file        =   models.FileField(blank=True, upload_to='challenges')
    ctf_url     =   models.URLField(blank=True)
    points      =   models.PositiveSmallIntegerField()
    slug        =   models.SlugField(max_length=55)
    pub_date    =   models.DateTimeField('Date published')
    category    =   models.ForeignKey(
                                       Category,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       )
    author        =   models.ForeignKey(User, unique=False, on_delete=models.CASCADE) 
    def solved_by(self, user):
        """True if the exercise has been solved by the user."""
        if not user.is_authenticated:
            return False
        try:
            CTF_flags.objects.get(user=user, ctf=self)
            return True
        except CTF_flags.DoesNotExist:
            return False
    
    def __str__(self):
        return self.name

class CTF_flags(models.Model):
    user        =   models.ForeignKey(User, unique=False, on_delete=models.CASCADE) 
    ctf         =   models.ForeignKey(CTF, unique=False, on_delete=models.CASCADE)
    flag_date   =   models.DateTimeField('Flag date')
    
    class Meta:
        ordering = ['-flag_date']
        verbose_name = 'solution'
        verbose_name_plural = 'solutions'
# Create your models here.
