from django.db import models

class new(models.Model):
    name        =   models.CharField(max_length=100)
    content     =   models.TextField(blank=True)
    content_en     =   models.TextField(blank=True)
    content_ru     =   models.TextField(blank=True)
    content_de     =   models.TextField(blank=True)
    slug        =   models.SlugField(max_length=55)
    pub_date    =   models.DateTimeField('Date published')
    def __str__(self):
        return self.name

# Create your models here.


