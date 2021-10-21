from django.contrib import admin
from .models import Event, Scores

#admin.site.register(Event)
#admin.site.register(Scores)

@admin.register(Event)
class event(admin.ModelAdmin):
    #list display
    list_display = ['name', 'start_date', 'end_date']
    # search list
    search_fields = ['name', 'slug', 'description', 'password']

@admin.register(Scores)
class score(admin.ModelAdmin):
    #list display
    list_display = ['user', 'event', 'score']
    #list Filter
    list_filter = ('event',)
    # search list
    search_fields = ['user__username', 'score', 'event__name']

# Register your models here.
