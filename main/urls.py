from django.urls import path
from .views import (
    AthleteListView, AthleteDetailView, AthleteCreateView, AthleteUpdateView, AthleteDeleteView,
    CoachListView, CoachDetailView, CoachCreateView, CoachUpdateView, CoachDeleteView,
    StaffListView, StaffDetailView, StaffCreateView, StaffUpdateView, StaffDeleteView,
    MediaListView, MediaDetailView, MediaCreateView, MediaUpdateView, MediaDeleteView,
    register, user_login, user_logout, CategoryListView, CategoryDetailView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    TeamListView, TeamDetailView, TeamCreateView, TeamUpdateView, TeamDeleteView,
    AthleteCategoryAssociationListView, AthleteCategoryAssociationDetailView, AthleteCategoryAssociationCreateView,
    AthleteCategoryAssociationUpdateView, AthleteCategoryAssociationDeleteView,
    TeamMembershipListView, TeamMembershipDetailView, TeamMembershipCreateView, TeamMembershipUpdateView,
    TeamMembershipDeleteView, register_athlete_coach
)
from . import views

urlpatterns = [
   # path('', home_redirect, name='home_redirect'),
    path('', views.dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('add/athlete', register_athlete_coach, name='register_athlete_coach'),

    # Athlete URLs
    path('athletes/', AthleteListView.as_view(), name='athlete_list'),
    path('athletes/<int:pk>/', AthleteDetailView.as_view(), name='athlete_detail'),
    path('athletes/create/', AthleteCreateView.as_view(), name='athlete_create'),
    path('athletes/<int:pk>/edit/', AthleteUpdateView.as_view(), name='athlete_edit'),
    path('athletes/<int:pk>/delete/', AthleteDeleteView.as_view(), name='athlete_delete'),

    # Coach URLs
    path('coaches/', CoachListView.as_view(), name='coach_list'),
    path('coaches/<int:pk>/', CoachDetailView.as_view(), name='coach_detail'),
    path('coaches/create/', CoachCreateView.as_view(), name='coach_create'),
    path('coaches/<int:pk>/edit/', CoachUpdateView.as_view(), name='coach_edit'),
    path('coaches/<int:pk>/delete/', CoachDeleteView.as_view(), name='coach_delete'),

    # Staff URLs
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff_detail'),
    path('staff/create/', StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/edit/', StaffUpdateView.as_view(), name='staff_edit'),
    path('staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff_delete'),

    # Media URLs
    path('media/', MediaListView.as_view(), name='media_list'),
    path('media/<int:pk>/', MediaDetailView.as_view(), name='media_detail'),
    path('media/create/', MediaCreateView.as_view(), name='media_create'),
    path('media/<int:pk>/edit/', MediaUpdateView.as_view(), name='media_edit'),
    path('media/<int:pk>/delete/', MediaDeleteView.as_view(), name='media_delete'),

    # Category URLs
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    # Team URLs
    path('teams/', TeamListView.as_view(), name='team_list'),
    path('teams/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('teams/add/', TeamCreateView.as_view(), name='team_add'),
    path('teams/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_edit'),
    path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),

    # AthleteCategoryAssociation URLs
    path('associations/', AthleteCategoryAssociationListView.as_view(), name='athlete_category_association_list'),
    path('associations/<int:pk>/', AthleteCategoryAssociationDetailView.as_view(), name='athlete_category_association_detail'),
    path('associations/add/', AthleteCategoryAssociationCreateView.as_view(), name='athlete_category_association_add'),
    path('associations/<int:pk>/edit/', AthleteCategoryAssociationUpdateView.as_view(), name='athlete_category_association_edit'),
    path('associations/<int:pk>/delete/', AthleteCategoryAssociationDeleteView.as_view(), name='athlete_category_association_delete'),

    # TeamMembership URLs
    path('memberships/', TeamMembershipListView.as_view(), name='team_membership_list'),
    path('memberships/<int:pk>/', TeamMembershipDetailView.as_view(), name='team_membership_detail'),
    path('memberships/add/', TeamMembershipCreateView.as_view(), name='team_membership_add'),
    path('memberships/<int:pk>/edit/', TeamMembershipUpdateView.as_view(), name='team_membership_edit'),
    path('memberships/<int:pk>/delete/', TeamMembershipDeleteView.as_view(), name='team_membership_delete'),

    path('male-coaches-athletes/', views.male_coaches_athletes, name='male_coaches_athletes'),
    path('female-coaches-athletes/', views.female_coaches_athletes, name='female_coaches_athletes'),
    path('all-coaches-athletes/', views.all_coaches_athletes, name='all_coaches_athletes'),
]
