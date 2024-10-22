from django.contrib import admin
from .models import UserProfile, Ability, WorkExperience, Application

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'resume') 
    search_fields = ('user__email', 'phone') 
    list_filter = ('abilities',)  

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'company', 'position', 'start_date', 'end_date')
    search_fields = ('user_profile__user__email', 'company__name', 'position__name')
    list_filter = ('company', 'position')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Ability)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Application)