from .models import UserProfileInfo
from django.contrib import admin

#admin.site.register(UserProfileInfo)
# Register your models here.

@admin.register(UserProfileInfo)
class userprofile(admin.ModelAdmin):
    #list display
    list_display = ['user', 'score', 'last_submission_date']
    # search list
    search_fields = ['score', 'user__username']