from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from .forms import *
from .models import Athlete, Coach, Staff, Media, RoleType, Category, Country, Belt, Team, Membership, Tournament, TournamentParticipation
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from main1.utils import *
from django.conf import settings
from django.core.files.storage import default_storage
import os
from django.contrib import messages
import logging
from django.http import HttpResponse
from fillpdf import fillpdfs
import datetime
from .utils import *
logger = logging.getLogger(__name__)

@login_required
def coach_dashboard(request):
    try:
        # Get the coach associated with the logged-in user
        coach = Coach.objects.get(user=request.user)
        
        # Filter active athletes for the coach
        active_athletes = Athlete.objects.filter(coach=coach, is_active=True)
        
        # Get upcoming tournaments
        upcoming_tournaments = Tournament.objects.filter(start_date__gte=datetime.date.today()).order_by('start_date')

        # Prepare context with relevant data
        context = {
            'active_athletes': active_athletes,
            'coach': coach,
            'upcoming_tournaments': upcoming_tournaments,  # Include upcoming tournaments
        }
        
        # Render the coach dashboard template
        return render(request, 'index1.html', context)
    
    except Coach.DoesNotExist:
        # Handle the case where no coach is found for the logged-in user
        return render(request, 'no_coach.html', {'message': 'You are not assigned as a coach.'})

@login_required
def register_athletes(request, tournament_id):
    # Get the tournament object using the provided tournament_id
    tournament = get_object_or_404(Tournament, id=tournament_id)

    # If the form is submitted (POST request)
    if request.method == 'POST':
        # Create a form instance using the POST data and pass the tournament
        form = AthleteSelectionForm(request.POST, tournament=tournament)
        if form.is_valid():
            # Get the selected athletes from the form
            selected_athletes = form.cleaned_data['athletes']
            
            # Iterate through the selected athletes and register them for the tournament
            for athlete in selected_athletes:
                # Ensure the athlete is not already participating in the tournament
                if not TournamentParticipation.objects.filter(
                    tournament=tournament,
                    athlete=athlete
                ).exists():
                    # Create a new participation record
                    TournamentParticipation.objects.create(
                        tournament=tournament,
                        athlete=athlete
                    )

            # Redirect to the tournament detail page after successful registration
            return redirect('tournament_details', tournament_id=tournament.id)
    else:
        # If it's a GET request, show an empty form
        form = AthleteSelectionForm(tournament=tournament)

    # Render the form in the template with the tournament context
    return render(request, 'client/register_athletes.html', {
        'form': form,
        'tournament': tournament,
    })

# Athlete Views
@method_decorator(login_required, name='dispatch')
class AthleteListView(LoginRequiredMixin, ListView):
    model = Athlete
    template_name = 'athletes/athlete_list.html'
    context_object_name = 'athletes'

    def get_queryset(self):
        athletes = Athlete.objects.select_related('country', 'belt', 'accommodation').prefetch_related('category')
        coach_athletes = Coach.objects.filter(is_athlete=True).select_related('country', 'belt').prefetch_related('category')

        athletes_list = []
        for athlete in athletes:
            athlete_data = {
                'pk': athlete.pk,
                'name': athlete.name,
                'passport_photo': athlete.passport_photo.url if athlete.passport_photo else None,
                'country': athlete.country.name,
                'region': athlete.region.name if athlete.region else 'N/A',
                'id_passport_number': athlete.id_passport_number,
                'passport': athlete.passport,
                'dob': athlete.dob,
                'gender': athlete.gender,
                'contacts': athlete.contacts,
                'arrival_date': athlete.arrival_date,
                'departure_date': athlete.departure_date,
                'accommodation': athlete.accommodation.name if athlete.accommodation else 'N/A',
                'weight': athlete.weight,
                'belt': athlete.belt.name if athlete.belt else 'N/A',
                'category': list(athlete.category.values_list('name', flat=True)),
                'age': athlete.age,
                'get_weight_category': athlete.get_weight_category,
            }
            athletes_list.append(athlete_data)

        for coach in coach_athletes:
            coach_data = {
                'pk': coach.pk,
                'name': coach.name,
                'passport_photo': coach.passport_photo.url if coach.passport_photo else None,
                'country': coach.country.name,
                'region': coach.region.name if coach.region else 'N/A',
                'id_passport_number': coach.id_passport_number,
                'passport': coach.passport,
                'dob': coach.dob,
                'gender': coach.gender,
                'contacts': coach.contacts,
                'arrival_date': coach.arrival_date,
                'departure_date': coach.departure_date,
                'accommodation': coach.accommodation.name if coach.accommodation else 'N/A',
                'weight': coach.weight,
                'belt': coach.belt.name if coach.belt else 'N/A',
                'category': list(coach.category.values_list('name', flat=True)),
                'age': coach.age,
                'get_weight_category': coach.get_weight_category,
            }
            athletes_list.append(coach_data)

        return athletes_list

@method_decorator(login_required, name='dispatch')
class AthleteDetailView(DetailView):
    model = Athlete
    template_name = 'athletes/athlete_detail.html'
    context_object_name = 'athlete'

@method_decorator(login_required, name='dispatch')
class AthleteCreateView(CreateView):
    model = Athlete
    form_class = AthleteForm
    template_name = 'athletes/athlete_form.html'
    success_url = reverse_lazy('athlete_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.category.set(form.cleaned_data['category'])
        return response

@method_decorator(login_required, name='dispatch')
class AthleteUpdateView(UpdateView):
    model = Athlete
    form_class = AthleteUpdateForm
    template_name = 'athletes/update.html'
    success_url = reverse_lazy('athlete_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.category.set(form.cleaned_data['category'])
        return response

@method_decorator(login_required, name='dispatch')
class AthleteDeleteView(DeleteView):
    model = Athlete
    template_name = 'athletes/athlete_confirm_delete.html'
    success_url = reverse_lazy('athlete_list')

# Coach Views
@method_decorator(login_required, name='dispatch')
class CoachListView(ListView):
    model = Coach
    template_name = 'coach/coach_list.html'
    context_object_name = 'coaches'

@method_decorator(login_required, name='dispatch')
class CoachDetailView(DetailView):
    model = Coach
    template_name = 'coach/coach_detail.html'
    context_object_name = 'coach'

@method_decorator(login_required, name='dispatch')
class CoachCreateView(CreateView):
    model = Coach
    form_class = CoachForm
    template_name = 'coach/coach_form.html'
    success_url = reverse_lazy('coach_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.category.set(form.cleaned_data['category'])
        return response

@method_decorator(login_required, name='dispatch')
class CoachUpdateView(UpdateView):
    model = Coach
    form_class = CoachForm
    template_name = 'coach/coach_update.html'
    success_url = reverse_lazy('coach_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.category.set(form.cleaned_data['category'])
        return response

@method_decorator(login_required, name='dispatch')
class CoachDeleteView(DeleteView):
    model = Coach
    template_name = 'coach/coach_confirm_delete.html'
    success_url = reverse_lazy('coach_list')

# Staff Views
@method_decorator(login_required, name='dispatch')
class StaffListView(ListView):
    model = Staff
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff_members'

@method_decorator(login_required, name='dispatch')
class StaffDetailView(DetailView):
    model = Staff
    template_name = 'staff/staff_detail.html'
    context_object_name = 'staff'

@method_decorator(login_required, name='dispatch')
class StaffCreateView(CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff_list')

@method_decorator(login_required, name='dispatch')
class StaffUpdateView(UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'staff/staff_update.html'
    success_url = reverse_lazy('staff_list')

@method_decorator(login_required, name='dispatch')
class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'staff/staff_confirm_delete.html'
    success_url = reverse_lazy('staff_list')

# Media Views
@method_decorator(login_required, name='dispatch')
class MediaListView(ListView):
    model = Media
    template_name = 'media/media_list.html'
    context_object_name = 'media_list'

@method_decorator(login_required, name='dispatch')
class MediaDetailView(DetailView):
    model = Media
    template_name = 'media/media_detail.html'
    context_object_name = 'media'

@method_decorator(login_required, name='dispatch')
class MediaCreateView(CreateView):
    model = Media
    form_class = MediaForm
    template_name = 'media/media_form.html'
    success_url = reverse_lazy('media_list')

@method_decorator(login_required, name='dispatch')
class MediaUpdateView(UpdateView):
    model = Media
    form_class = MediaForm
    template_name = 'media/media_update.html'
    success_url = reverse_lazy('media_list')

@method_decorator(login_required, name='dispatch')
class MediaDeleteView(DeleteView):
    model = Media
    template_name = 'media/media_confirm_delete.html'
    success_url = reverse_lazy('media_list')

# Gender-Specific Views
@login_required
def male_coaches_athletes(request):
    male_coaches = Coach.objects.filter(gender='Male')
    male_athletes = Athlete.objects.filter(gender='Male')
    context = {
        'coaches': male_coaches,
        'athletes': male_athletes
    }
    return render(request, 'links/male_coaches_athletes.html', context)

@login_required
def female_coaches_athletes(request):
    female_coaches = Coach.objects.filter(gender='Female')
    female_athletes = Athlete.objects.filter(gender='Female')
    context = {
        'coaches': female_coaches,
        'athletes': female_athletes
    }
    return render(request, 'links/female_coaches_athletes.html', context)

@login_required
def all_coaches_athletes(request):
    coaches = Coach.objects.all()
    athletes = Athlete.objects.all()
    context = {
        'coaches': coaches,
        'athletes': athletes
    }
    return render(request, 'links/all_coaches_athletes.html', context)

# Team Views
@method_decorator(login_required, name='dispatch')
class TeamListView(ListView):
    model = Team
    template_name = 'teams/team_list.html'
    context_object_name = 'teams'

@method_decorator(login_required, name='dispatch')
class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_detail.html'
    context_object_name = 'team'

@method_decorator(login_required, name='dispatch')
class TeamCreateView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('team_list')

@method_decorator(login_required, name='dispatch')
class TeamUpdateView(UpdateView):
    model = Team
    form_class = TeamForm
    template_name = 'teams/team_form.html'
    success_url = reverse_lazy('team_list')

@method_decorator(login_required, name='dispatch')
class TeamDeleteView(DeleteView):
    model = Team
    template_name = 'teams/team_confirm_delete.html'
    success_url = reverse_lazy('team_list')

# Membership Management Views
@login_required
def add_member(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.team = team
            member.save()
            return redirect('team_detail', pk=team.pk)
    else:
        form = MembershipForm()
    return render(request, 'team_memberships/members_form.html', {'form': form, 'team': team})
@login_required
def check_and_redirect(request):
    if Coach.objects.filter(user=request.user).exists():
        return redirect('coach_dashboard')
    # Redirect to a default page or raise an exception
    return redirect('home') 
class CoachRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if Coach.objects.filter(user=request.user).exists():
            return redirect('coach_dashboard')
        return super().dispatch(request, *args, **kwargs)
    
@login_required
def TournamentListView(request):
    if Coach.objects.filter(user=request.user).exists():
        return redirect('coach_dashboard')
    tournaments = Tournament.objects.all()
    context = {'tournaments': tournaments}
    return render(request, 'tournament/tournament_list.html', context)


class TournamentCreateView(CreateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournament/tournament_form.html'
    success_url = reverse_lazy('tournament_list')


class TournamentDetailsView( DetailView):
    model = Tournament
    template_name = 'tournament/tournament_detail.html'
    context_object_name = 'tournament'
    pk_url_kwarg = 'tournament_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()  # Get the Tournament object

        # Get the logged-in user
        user = self.request.user
        
        
        # Calculate total participants and total countries
        total_participants = TournamentParticipation.objects.filter(tournament=tournament).count()
        total_countries = TournamentParticipation.objects.filter(tournament=tournament).values('athlete__country').distinct().count()

        # Add the data to the context
        context['total_participants'] = total_participants
        context['total_countries'] = total_countries
        

        return context
    
class TournamentDetailsViewCoach(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = 'tournament/tournament_detail.html'
    context_object_name = 'tournament'
    pk_url_kwarg = 'tournament_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = self.get_object()  # Get the Tournament object

        # Get the logged-in user
        user = self.request.user
        
        # Retrieve coach based on the user
        coach = get_coach_for_user(user.id)
        if coach:
            coach_id = coach.id
        else:
            coach_id = None

        # Calculate total participants and total countries
        total_participants = TournamentParticipation.objects.filter(tournament=tournament).count()
        total_countries = TournamentParticipation.objects.filter(tournament=tournament).values('athlete__country').distinct().count()

        # Add the data to the context
        context['total_participants'] = total_participants
        context['total_countries'] = total_countries
        context['coach_id'] = coach_id  # Add coach_id to the context if needed

        return context    
class TournamentUpdateView(UpdateView):
    model = Tournament
    form_class = TournamentForm
    template_name = 'tournament/tournament_form.html'
    success_url = reverse_lazy('tournament_list')

class TournamentDeleteView(DeleteView):
    model = Tournament
    template_name = 'tournament/tournament_confirm_delete.html'
    success_url = reverse_lazy('tournament_list')


class TournamentParticipationListView( ListView):
    model = TournamentParticipation
    template_name = 'tournament/tournament_participation_list.html'
    context_object_name = 'participations'


@login_required
def generate_pdf(request, tournament_id, athlete_id):
    print(f"Starting PDF generation for tournament ID: {tournament_id} and athlete ID: {athlete_id}")
    
    # Fetch tournament and athlete
    tournament = get_object_or_404(Tournament, id=tournament_id)
    athlete = get_object_or_404(Athlete, id=athlete_id)
    
    # Define the template and output paths
    pdf_template_path = os.path.join(settings.MEDIA_ROOT, 'doc', 'MO2024 INVITATION LETTER -  REG FORM1.pdf')
    pdf_output_dir = os.path.join(settings.MEDIA_ROOT, 'completed_forms')
    os.makedirs(pdf_output_dir, exist_ok=True)  # Ensure the output directory exists

    pdf_output_path = os.path.join(pdf_output_dir, f'{athlete.name}_{tournament.edition}th Edition Consent Form.pdf')

    FIELD_MAPPING = {
        'Family Name': 'Text1',
        'Given names': 'Text2',
        'Gender': 'Text3',
        'Birthday': 'Text4',
        'Age': 'Text5',
        'Weight': 'Text6',
        'Nationality': 'Text7',
        'Postal Address': 'Text8',
        'Email': 'Text9',
        'Telephone': 'Text10',
        'Martial Arts Style': 'Text11',
        'Instructor': 'Text12',
        'Rank': 'Text13',
        'Forms Competition': 'Check1',  # Assuming checkbox field names
        'Special Techniques': 'Check2',
        'Free Sparring': 'Check3',
        'Competitor’s complete names': 'Text14',
        'Competitor’s Signature': 'Text15',
        'Date': 'Text16',
    }

    # Create athlete data
    def get_category_checks(athlete):
        categories = athlete.category.all()
        
        check1 = 'Yes' if any(category.name == 'individual_form' for category in categories) else 'No'
        check2 = 'Yes' if any(category.name == 'special_technique' for category in categories) else 'No'
        check3 = 'Yes' if any(category.name == 'sparring' for category in categories) else 'No'
        
        return {
            'check1': check1,
            'Check2': check2,
            'Check3': check3,
        }

    # Generating athlete data for PDF
    athlete_data = {
        'Text1': athlete.name.split(' ')[-1] if athlete.name else '',
        'Text2': ' '.join(athlete.name.split(' ')[:-1]) if athlete.name else '',
        'Text3': athlete.gender if athlete.gender else '',
        'Text16': athlete.dob.strftime('%d-%m-%Y') if athlete.dob else '',
        'Text4': athlete.age if athlete.age else '',
        'Text5': str(athlete.weight) if athlete.weight else '',
        'Text6': athlete.country.name if athlete.country and athlete.country.name else '',
        'Text7': athlete.email if athlete.email else '',
        'Text8': athlete.email if athlete.email else '',
        'Text9': athlete.contacts if athlete.contacts else '',
        'Text10': str(athlete.belt) if athlete.belt else '',
        'Text11': athlete.coach.name if athlete.coach else '',
        'Text12': str(athlete.coach.belt) if athlete.coach and athlete.coach.belt else '',
        'Text13': athlete.name if athlete.name else '',
        'Text14': '',  # Add actual signature handling if necessary
        'Text15': datetime.datetime.today().strftime('%d-%m-%Y'),  # Use current date
    }

    # Add category checks to the athlete data
    category_checks = get_category_checks(athlete)
    athlete_data.update(category_checks)

    # Check if form fields are correctly retrieved
    form_fields = fillpdfs.get_form_fields(pdf_template_path)

    if not all(field in form_fields for field in athlete_data.keys()):
        return HttpResponse("Error: Some form fields are missing", status=400)

    # Fill the PDF
    try:
        fillpdfs.write_fillable_pdf(
            input_pdf_path=pdf_template_path,
            output_pdf_path=pdf_output_path,
            data_dict={FIELD_MAPPING.get(k, k): v for k, v in athlete_data.items()}
        )
        print(f"PDF successfully saved to {pdf_output_path}")

        # Return the PDF as an HttpResponse for direct download
        with open(pdf_output_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_output_path)}"'
            return response

    except Exception as e:
        print(f"Error generating PDF for athlete {athlete.id}: {e}")
        return HttpResponse("Error generating PDF", status=500)
    else:
        return HttpResponse("No participations found", status=404)

class TournamentParticipationCreateView(CreateView):
    model = TournamentParticipation
    form_class = TournamentParticipationForm
    template_name = 'tournament/tournament_participation_form.html'
    success_url = reverse_lazy('tournament_participation_list')

class TournamentParticipationUpdateView(UpdateView):
    model = TournamentParticipation
    form_class = TournamentParticipationForm
    template_name = 'tournament/tournament_participation_form.html'
    success_url = reverse_lazy('tournament_participation_list')

class TournamentParticipationDeleteView(DeleteView):
    model = TournamentParticipation
    template_name = 'tournament/tournament_participation_confirm_delete.html'
    success_url = reverse_lazy('tournament_participation_list')

# Authentication Views
class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')



