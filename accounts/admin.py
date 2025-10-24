from django.contrib import admin
from django.contrib.auth.models import User
from main1.models import Coach

class CoachSuperAdmin(admin.ModelAdmin):
    actions = ['link_user_to_coach']

    def link_user_to_coach(self, request, queryset):
        for coach in queryset:
            # Your logic to link the selected coaches to their users
            pass

