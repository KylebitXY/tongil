from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout, authenticate
from .models import Athlete, Coach, Staff, Media, Category, Team, AthleteCategoryAssociation, TeamMembership
from .forms import AthleteForm, CoachForm, StaffForm, MediaForm, CategoryForm, TeamForm, AthleteCategoryAssociationForm, TeamMembershipForm, UserRegistrationForm, LoginForm
from .forms import AthleteCoachForm
from django.db import IntegrityError


def register_athlete_coach(request):
    if request.method == 'POST':
        form = AthleteCoachForm(request.POST, request.FILES)
        if form.is_valid():
            # Assuming the form combines fields for athlete and coach
            athlete_data = {
                'id_passport_number': form.cleaned_data.get('id_passport_number'),
                'name': form.cleaned_data.get('name'),
                'country': form.cleaned_data.get('country'),
                # Add all other necessary fields here
            }
            
            try:
                athlete, created = Athlete.objects.get_or_create(
                    id_passport_number=athlete_data['id_passport_number'],
                    defaults=athlete_data
                )
                
                if not created:
                    # Update the existing athlete's data if needed
                    for key, value in athlete_data.items():
                        setattr(athlete, key, value)
                    athlete.save()

                # Handle coach data here
                coach_data = {
                    # Extract coach fields similarly
                }

                # Create or update coach, associate with athlete, etc.

                return redirect('athlete_list')

            except IntegrityError:
                form.add_error('id_passport_number', 'Athlete with this ID already exists.')

    else:
        form = AthleteCoachForm()
    
    return render(request, 'registration/all.html', {'form': form})

def dashboard(request):
    total_males = Coach.objects.filter(gender='Male').count() + Athlete.objects.filter(gender='Male').count()
    total_females = Coach.objects.filter(gender='Female').count() + Athlete.objects.filter(gender='Female').count()
    total_coaches = Coach.objects.count()
    total_athletes = Athlete.objects.count()
    overall_total = total_coaches + total_athletes

    context = {
        'total_males': total_males,
        'total_females': total_females,
        'total_coaches': total_coaches,
        'total_athletes': total_athletes,
        'overall_total': overall_total,
    }
    return render(request, 'index.html', context)
# Mixin for login required decorator
class LoginRequiredMixin:
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# Base class for handling CRUD operations
class BaseModelView(LoginRequiredMixin):
    model = None
    form_class = None
    template_name = None
    success_url = None

    def get_template_names(self):
        if not self.template_name:
            raise ValueError("template_name isn't set")
        return [self.template_name]

    def get_success_url(self):
        if not self.success_url:
            raise ValueError("success_url isn't set")
        return self.success_url

# List View
class BaseListView(BaseModelView, ListView):
    template_name_suffix = '_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.model.__name__.lower() + 's'] = self.get_queryset()
        return context

# Detail View
class BaseDetailView(BaseModelView, DetailView):
    template_name_suffix = '_detail'

# Create View
class BaseCreateView(BaseModelView, CreateView):
    template_name_suffix = '_form'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return redirect(self.get_success_url())

# Update View
class BaseUpdateView(BaseModelView, UpdateView):
    template_name_suffix = '_form'

# Delete View
class BaseDeleteView(BaseModelView, DeleteView):
    template_name_suffix = '_confirm_delete'


# Athlete Views
class AthleteListView(BaseListView):
    model = Athlete
    template_name = 'athletes/athlete_list.html'

class AthleteDetailView(BaseDetailView):
    model = Athlete
    template_name = 'athletes/athlete_detail.html'

class AthleteCreateView(BaseCreateView):
    model = Athlete
    form_class = AthleteForm
    template_name = 'athletes/athlete_form.html'
    success_url = reverse_lazy('athlete_list')

class AthleteUpdateView(BaseUpdateView):
    model = Athlete
    form_class = AthleteForm
    template_name = 'athletes/athlete_form.html'
    success_url = reverse_lazy('athlete_list')

class AthleteDeleteView(BaseDeleteView):
    model = Athlete
    template_name = 'athletes/athlete_confirm_delete.html'
    success_url = reverse_lazy('athlete_list')

# Coach Views
class CoachListView(BaseListView):
    model = Coach
    template_name = 'coach/coach_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['coaches'] = self.get_queryset()
        
        return context


class CoachDetailView(BaseDetailView):
    model = Coach
    template_name = 'coach/coach_detail.html'

class CoachCreateView(BaseCreateView):
    model = Coach
    form_class = CoachForm
    template_name = 'coach/coach_form.html'
    success_url = reverse_lazy('coach_list')

class CoachUpdateView(BaseUpdateView):
    model = Coach
    form_class = CoachForm
    template_name = 'coach/coach_form.html'
    success_url = reverse_lazy('coach_list')

class CoachDeleteView(BaseDeleteView):
    model = Coach
    template_name = 'coach/coach_confirm_delete.html'
    success_url = reverse_lazy('coach_list')

# Staff Views
class StaffListView(BaseListView):
    model = Staff
    template_name = 'staff/staff_list.html'

class StaffDetailView(BaseDetailView):
    model = Staff
    template_name = 'staff/staff_detail.html'

class StaffCreateView(BaseCreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_list')

class StaffUpdateView(BaseUpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_list')

class StaffDeleteView(BaseDeleteView):
    model = Staff
    template_name = 'staff/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_list')

# Media Views
class MediaListView(BaseListView):
    model = Media
    template_name = 'media/media_list.html'

class MediaDetailView(BaseDetailView):
    model = Media
    template_name = 'media/media_detail.html'

class MediaCreateView(BaseCreateView):
    model = Media
    form_class = MediaForm
    template_name = 'media/media_form.html'
    success_url = reverse_lazy('media_list')

class MediaUpdateView(BaseUpdateView):
    model = Media
    form_class = MediaForm
    template_name = 'media/media_form.html'
    success_url = reverse_lazy('media_list')

class MediaDeleteView(BaseDeleteView):
    model = Media
    template_name = 'media/media_confirm_delete.html'
    success_url = reverse_lazy('media_list')

# Category Views
class CategoryListView(BaseListView):
    model = Category
    template_name = 'categories/category_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_queryset()
        
        return context

class CategoryDetailView(BaseDetailView):
    model = Category
    template_name = 'categories/category_detail.html'

class CategoryCreateView(BaseCreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(BaseUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'categories/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(BaseDeleteView):
    model = Category
    template_name = 'categories/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

# Team Views
class TeamListView(BaseListView):
    model = Team
    template_name = 'teams/team_list.html'
    

class TeamDetailView(BaseDetailView):
    model = Team
    template_name = 'teams/team_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all athletes associated with this team
        context['team_memberships'] = TeamMembership.objects.filter(team=self.object)
        return context


class TeamCreateView(BaseCreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('team_list')

class TeamUpdateView(BaseUpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('team_list')

class TeamDeleteView(BaseDeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('team_list')

# AthleteCategoryAssociation Views
class AthleteCategoryAssociationListView(BaseListView):
    model = AthleteCategoryAssociation
    template_name = 'athlete_category/association_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['associations'] = self.get_queryset()
        
        return context

class AthleteCategoryAssociationDetailView(BaseDetailView):
    model = AthleteCategoryAssociation
    template_name = 'athlete_category/association_detail.html'

class AthleteCategoryAssociationCreateView(BaseCreateView):
    model = AthleteCategoryAssociation
    form_class = AthleteCategoryAssociationForm
    template_name = 'athlete_category/association_form.html'
    success_url = reverse_lazy('athlete_category_association_list')

class AthleteCategoryAssociationUpdateView(BaseUpdateView):
    model = AthleteCategoryAssociation
    form_class = AthleteCategoryAssociationForm
    template_name = 'athlete_category/association_form.html'
    success_url = reverse_lazy('athlete_category_association_list')

class AthleteCategoryAssociationDeleteView(BaseDeleteView):
    model = AthleteCategoryAssociation
    template_name = 'athlete_category/association_confirm_delete.html'
    success_url = reverse_lazy('athlete_category_association_list')

# TeamMembership Views
class TeamMembershipListView(BaseListView):
    model = TeamMembership
    template_name = 'team_memberships/membership_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_memberships'] = self.get_queryset()
        
        return context

class TeamMembershipDetailView(BaseDetailView):
    model = TeamMembership
    template_name = 'team_memberships/membership_detail.html'

class TeamMembershipCreateView(BaseCreateView):
    model = TeamMembership
    form_class = TeamMembershipForm
    template_name = 'team_memberships/membership_form.html'
    success_url = reverse_lazy('team_membership_list')

class TeamMembershipUpdateView(BaseUpdateView):
    model = TeamMembership
    form_class = TeamMembershipForm
    template_name = 'team_memberships/membership_form.html'
    success_url = reverse_lazy('team_membership_list')

class TeamMembershipDeleteView(BaseDeleteView):
    model = TeamMembership
    template_name = 'team_memberships/membership_confirm_delete.html'
    success_url = reverse_lazy('team_membership_list')

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

def male_coaches_athletes(request):
    # Query for male coaches and athletes
    male_coaches = Coach.objects.filter(gender='Male')
    male_athletes = Athlete.objects.filter(gender='Male')
    context = {
        'coaches': male_coaches,
        'athletes': male_athletes
    }
    return render(request, 'links/male_coaches_athletes.html', context)

def female_coaches_athletes(request):
    # Query for female coaches and athletes
    female_coaches = Coach.objects.filter(gender='Female')
    female_athletes = Athlete.objects.filter(gender='Female')
    context = {
        'coaches': female_coaches,
        'athletes': female_athletes
    }
    return render(request, 'links/female_coaches_athletes.html', context)

def all_coaches_athletes(request):
    # Query for all coaches and athletes
    all_coaches = Coach.objects.all()
    all_athletes = Athlete.objects.all()
    context = {
        'coaches': all_coaches,
        'athletes': all_athletes
    }
    return render(request, 'links/all_coaches_athletes.html', context)