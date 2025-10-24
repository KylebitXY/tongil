from django.urls import path
from .views import (
    
    AthleteListView, AthleteDetailView, AthleteCreateView, AthleteUpdateView, AthleteDeleteView,
    CoachListView, CoachDetailView, CoachCreateView, CoachUpdateView, CoachDeleteView,
    StaffListView, StaffDetailView, StaffCreateView, StaffUpdateView, StaffDeleteView,
    MediaListView, MediaDetailView, MediaCreateView, MediaUpdateView, MediaDeleteView,TeamListView, TeamDetailView, TeamCreateView, TeamUpdateView,
    TeamDeleteView, TournamentListView, TournamentCreateView, TournamentUpdateView, TournamentDeleteView,
    TournamentParticipationListView, TournamentParticipationCreateView, TournamentParticipationUpdateView, TournamentParticipationDeleteView, TournamentDetailsView
)
from . import views
from django.urls import path, include


urlpatterns = [
    

    path('athletes/', AthleteListView.as_view(), name='athlete_list'),
    path('athlete/<int:pk>/', AthleteDetailView.as_view(), name='athlete_detail'),
    path('athlete/create/', AthleteCreateView.as_view(), name='athlete_create'),
    path('athlete/update/<int:pk>/', AthleteUpdateView.as_view(), name='athlete_update'),
    path('athlete/delete/<int:pk>/', AthleteDeleteView.as_view(), name='athlete_delete'),

    path('coaches/', CoachListView.as_view(), name='coach_list'),
    path('coach/<int:pk>/', CoachDetailView.as_view(), name='coach_detail'),
    path('coach/create/', CoachCreateView.as_view(), name='coach_create'),
    path('coach/update/<int:pk>/', CoachUpdateView.as_view(), name='coach_update'),
    path('coach/delete/<int:pk>/', CoachDeleteView.as_view(), name='coach_delete'),

    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff_detail'),
    path('staff/create/', StaffCreateView.as_view(), name='staff_create'),
    path('staff/update/<int:pk>/', StaffUpdateView.as_view(), name='staff_update'),
    path('staff/delete/<int:pk>/', StaffDeleteView.as_view(), name='staff_delete'),

    path('media/', MediaListView.as_view(), name='media_list'),
    path('media/<int:pk>/', MediaDetailView.as_view(), name='media_detail'),
    path('media/create/', MediaCreateView.as_view(), name='media_create'),
    path('media/update/<int:pk>/', MediaUpdateView.as_view(), name='media_update'),
    path('media/delete/<int:pk>/', MediaDeleteView.as_view(), name='media_delete'),

     # Team URLs
    path('memberships/', TeamListView.as_view(), name='team_list'),
    path('memberships/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path('memberships/add/', TeamCreateView.as_view(), name='team_add'),
    path('memberships/<int:team_id>/add/', views.add_member, name='team_members_add'),
    path('memberships/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_edit'),
    path('memberships/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),

    path('male-coaches-athletes/', views.male_coaches_athletes, name='male_coaches_athletes'),
    path('female-coaches-athletes/', views.female_coaches_athletes, name='female_coaches_athletes'),
    path('all-coaches-athletes/', views.all_coaches_athletes, name='all_coaches_athletes'),

     # Tournament URLs
     path('', views.coach_dashboard, name='coach_dashboard'), 
    path('tournaments/', views.TournamentListView, name='tournament_list'),
    path('tournament/<int:tournament_id>/', TournamentDetailsView.as_view(), name='tournament_details'),
    path('tournament/<int:tournament_id>/register_athletes/', views.register_athletes, name='register_athletes'),
    path('generate-pdf/<int:tournament_id>/', views.generate_pdf, name='generate_pdf'),
    path('generate-pdf/<int:tournament_id>/<int:athlete_id>/', views.generate_pdf, name='generate_pdf_individual'), 
    path('tournaments/create/', TournamentCreateView.as_view(), name='tournament_create'),
    path('tournaments/<int:pk>/update/', TournamentUpdateView.as_view(), name='tournament_update'),
    path('tournaments/<int:pk>/delete/', TournamentDeleteView.as_view(), name='tournament_delete'),

    # Tournament Participation URLs
    path('tournament-participations', TournamentParticipationListView.as_view(), name='tournament_participation_list'),
    path('tournament-participations/create/', TournamentParticipationCreateView.as_view(), name='tournament_participation_create'),
    path('tournament-participations/<int:pk>/update/', TournamentParticipationUpdateView.as_view(), name='tournament_participation_update'),
    path('tournament-participations/<int:pk>/delete/', TournamentParticipationDeleteView.as_view(), name='tournament_participation_delete'),
]
