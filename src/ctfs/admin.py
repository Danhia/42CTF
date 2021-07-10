from django.contrib import admin
from .models import Category, CTF, CTF_flags

admin.site.register(Category)
admin.site.register(CTF)
admin.site.register(CTF_flags)

# Register your models here.
