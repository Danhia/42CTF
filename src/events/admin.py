from django.contrib import admin
from .models import Event, EventPlayer, Team

@admin.register(Event)
class event(admin.ModelAdmin):
    #list display
    list_display = ['name', 'start_date', 'end_date']
    # search list
    search_fields = ['name', 'slug', 'description', 'password']

@admin.register(EventPlayer)
class score(admin.ModelAdmin):
    #list display
    list_display = ['user', 'event', 'score']
    #list Filter
    list_filter = ('event',)
    # search list
    search_fields = ['user__username', 'score', 'event__name']

# Register your models here.

@admin.register(Team)
class team(admin.ModelAdmin):
    #list display
    list_display = ['name', 'password']
    #list Filter
    list_filter = ('event',)
    # search list
    search_fields = ['name']
