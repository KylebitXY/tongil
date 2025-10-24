from django.contrib import admin
from .models import Athlete, Coach, Staff, Media, Country, Belt, Work, Category, Team, AthleteCategoryAssociation, TeamMembership

@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'id_passport_number', 'dob', 'gender', 'belt', 'contacts', 'arrival_date', 'accommodation')
    search_fields = ('name', 'id_passport_number', 'country__name')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category__name')

@admin.register(AthleteCategoryAssociation)
class AthleteCategoryAssociationAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'category', 'date_registered')
    search_fields = ('athlete__name', 'category__name')

@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('athlete', 'team', 'role')
    search_fields = ('athlete__name', 'team__name')

# Also register the other models
admin.site.register(Coach)
admin.site.register(Staff)
admin.site.register(Media)
admin.site.register(Country)
admin.site.register(Belt)
admin.site.register(Work)
