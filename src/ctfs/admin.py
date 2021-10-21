from django.contrib import admin
from .models import Category, CTF, CTF_flags

admin.site.register(Category)
#admin.site.register(CTF)
#admin.site.register(CTF_flags)

@admin.register(CTF_flags)
class ctf_flags(admin.ModelAdmin):
    #list display
    list_display = ['user', 'ctf', 'flag_date']
    #list Filter
    list_filter = ('ctf__category', 'ctf', 'user','flag_date')
    # search list
    search_fields = ['ctf__category__name', 'ctf__name', 'user__username']

@admin.register(CTF)
class ctf(admin.ModelAdmin):
    #list display
    list_display = ['name', 'event', 'category']
    #list Filter
    list_filter = ('category', 'event')
    # search list
    search_fields = ['category__name', 'name', 'author__username']
# Register your models here.
