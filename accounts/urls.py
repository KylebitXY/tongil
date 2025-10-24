from django.urls import path
from main1.urls import *
from . import views
from .views import UserLogoutView
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', UserLogoutView.as_view(next_page='login'), name='logout'),
]
