from django import forms
from .models import Coach, Athlete, Staff, Media, Category, RoleType, Belt, Country, Team, Membership
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import *
from django.db.models import Q
class DateInput(forms.DateInput):
    input_type = 'date'

class CoachForm(forms.ModelForm):
    

    class Meta:
        model = Coach
        fields = [
            'name', 'passport_photo', 'country', 'region', 'id_passport_number', 
            'passport', 'passport_date_of_issue', 'passport_place_of_issue', 
            'passport_expiry_date', 'dob', 'gender', 'email', 'contacts', 
            'blood_group', 'arrival_date', 'departure_date', 'accommodation', 
            'is_athlete', 'level', 'belt', 'weight', 'category', 'email'
        ]
        widgets = {
            'dob': DateInput(),
            'passport_date_of_issue': DateInput(),
            'passport_expiry_date': DateInput(),
            'arrival_date': DateInput(),
            'departure_date': DateInput(),
            'region': forms.Select(attrs={'class': 'form-control', 'style': 'display:none;'}),  # Default hidden
            'country': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_athlete = cleaned_data.get("is_athlete")

        if is_athlete:
            # Require weight and category fields if the coach is also an athlete
            if not cleaned_data.get("weight"):
                self.add_error("weight", "Weight is required for athletes.")
            if not cleaned_data.get("category"):
                self.add_error("category", "Category is required for athletes.")
        else:
            # If not an athlete, ensure weight and category are not required
            cleaned_data['weight'] = None
            cleaned_data['category'] = None

        return cleaned_data

class AthleteForm(forms.ModelForm):
    
    class Meta:
        model = Athlete
        fields = [
            'name', 'passport_photo', 'country', 'region', 'id_passport_number', 
            'passport', 'passport_date_of_issue', 'passport_place_of_issue', 
            'passport_expiry_date', 'dob', 'gender', 'email', 'contacts', 
            'blood_group', 'arrival_date', 'departure_date', 'accommodation', 
            'weight', 'category', 'belt', 'coach', 'teams', 'email'
        ]
        widgets = {
            'dob': DateInput(),
            'passport_date_of_issue': DateInput(),
            'passport_expiry_date': DateInput(),
            'arrival_date': DateInput(),
            'departure_date': DateInput(),
            'region': forms.Select(attrs={'class': 'form-control'}),  # Default hidden
            'country': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(),
        }
class AthleteUpdateForm(forms.ModelForm):
   
    class Meta:
        model = Athlete
        fields = [
            'name', 'passport_photo', 'country', 'region', 'id_passport_number', 
            'passport', 'passport_date_of_issue', 'passport_place_of_issue', 
            'passport_expiry_date', 'dob', 'gender', 'email', 'contacts', 
            'blood_group', 'arrival_date', 'departure_date', 'accommodation', 
            'weight', 'category', 'belt', 'coach', 'teams', 'email'
        ]
        widgets = {
            'dob': DateInput(),
            'passport_date_of_issue': DateInput(),
            'passport_expiry_date': DateInput(),
            'arrival_date': DateInput(),
            'departure_date': DateInput(),
            'region': forms.Select(attrs={'class': 'form-control', }),  # Default hidden
            'country': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.SelectMultiple(),
        }
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'passport_photo', 'name', 'gender', 'id_passport_number', 'role', 
            'contacts'
        ]
        widgets = {
            'role': forms.Select(choices=Staff.ROLE_CHOICES),
            'gender': forms.Select(choices=Staff.GENDER_CHOICES),
        }

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = [
            'passport_photo', 'name', 'id_passport_number', 'gender', 'role', 
            'contacts', 'media_house'
        ]
        widgets = {
            'role': forms.Select(choices=Media.ROLE_CHOICES),
            'gender': forms.Select(choices=Media.GENDER_CHOICES),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class RoleTypeForm(forms.ModelForm):
    class Meta:
        model = RoleType
        fields = ['name']

class BeltForm(forms.ModelForm):
    class Meta:
        model = Belt
        fields = ['name']

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['name']

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation  # Assuming an Accommodation model exists
        fields = ['name', 'address', 'contact_number']


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'country', 'category', 'members']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(name__in=[
            'team_form', 'team_sparring', 'team_special_technique'
        ])

class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['team', 'athlete', 'joined_date']
        widgets = {
            'joined_date': DateInput(),
        }


class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'edition', 'start_date', 'end_date', 'location']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TournamentParticipationForm(forms.ModelForm):
    class Meta:
        model = TournamentParticipation
        fields = ['tournament', 'coach', 'athlete', 'category', 'performance']
        widgets = {
            'performance': forms.Textarea(attrs={'rows': 3}),
        }        

# JavaScript code to handle the display of the region field based on country selection
class AthleteSelectionForm(forms.Form):
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.none(),  # Start with no athletes
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        tournament = kwargs.pop('tournament', None)  # Removed coach
        super().__init__(*args, **kwargs)

        # Set the queryset for athletes, e.g., filtering athletes not already in the tournament
        if tournament:
            self.fields['athletes'].queryset = Athlete.objects.filter(
                ~Q(tournamentparticipation__tournament=tournament)
            )

class AthleteSelectionFormCoach(forms.Form):
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.none(),  # Start with no athletes
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        tournament = kwargs.pop('tournament', None)
        coach = kwargs.pop('coach', None)
        super().__init__(*args, **kwargs)
        
        if coach:
            # Filter athletes based on the coach's region/club
            if coach.region:
                self.fields['athletes'].queryset = Athlete.objects.filter(
                    region=coach.region
                )
            else:
                self.fields['athletes'].queryset = Athlete.objects.filter(
                    coach=coach
                )