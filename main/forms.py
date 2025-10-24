from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
class AthleteCoachForm(forms.Form):
    # Common fields
    name = forms.CharField(max_length=100, required=True)
    passport_photo = forms.ImageField(required=True)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=True)
    id_passport_number = forms.CharField(max_length=50, required=True)
    dob = forms.DateField(widget=forms.SelectDateWidget(years=range(1950, 2024)), required=True)
    gender = forms.ChoiceField(choices=Athlete.GENDER_CHOICES, required=True)
    contacts = forms.CharField(max_length=100, required=True)
    arrival_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2024, 2030)), required=True)
    departure_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2024, 2030)), required=True)
    accommodation = forms.CharField(max_length=100, required=False)

    # Athlete-specific fields
    is_athlete = forms.BooleanField(required=False, label="Register as Athlete")
    weight = forms.DecimalField(max_digits=5, decimal_places=2, required=False, label="Athlete's Weight")
    belt = forms.ModelChoiceField(queryset=Belt.objects.all(), required=False)

    # Coach-specific fields
    is_coach = forms.BooleanField(required=False, label="Register as Coach")
    coach_level = forms.ChoiceField(choices=Coach.LEVEL_CHOICES, required=False, label="Coach Level")
    region = forms.CharField(max_length=100, required=False)

    def save(self):
        data = self.cleaned_data
        athlete = None
        coach = None

        # Save Athlete
        if data.get('is_athlete'):
            athlete, created = Athlete.objects.get_or_create(
                id_passport_number=data['id_passport_number'],
                defaults={
                    'name': data['name'],
                    'passport_photo': data['passport_photo'],
                    'country': data['country'],
                    'dob': data['dob'],
                    'gender': data['gender'],
                    'weight': data['weight'],
                    'belt': data['belt'],
                    'contacts': data['contacts'],
                    'arrival_date': data['arrival_date'],
                    'departure_date': data['departure_date'],
                    'accommodation': data['accommodation'],
                }
            )
            if not created:
                # Update the existing athlete's data if necessary
                athlete.name = data['name']
                athlete.passport_photo = data['passport_photo']
                athlete.country = data['country']
                athlete.dob = data['dob']
                athlete.gender = data['gender']
                athlete.weight = data['weight']
                athlete.belt = data['belt']
                athlete.contacts = data['contacts']
                athlete.arrival_date = data['arrival_date']
                athlete.departure_date = data['departure_date']
                athlete.accommodation = data['accommodation']
                athlete.save()

        # Save Coach
        if data.get('is_coach'):
            coach, created = Coach.objects.get_or_create(
                id_passport_number=data['id_passport_number'],
                defaults={
                    'name': data['name'],
                    'passport_photo': data['passport_photo'],
                    'country': data['country'],
                    'region': data['region'],
                    'dob': data['dob'],
                    'gender': data['gender'],
                    'belt': data['belt'],
                    'level': data['coach_level'],
                    'contacts': data['contacts'],
                    'arrival_date': data['arrival_date'],
                    'departure_date': data['departure_date'],
                    'accommodation': data['accommodation'],
                }
            )
            if not created:
                # Update the existing coach's data if necessary
                coach.name = data['name']
                coach.passport_photo = data['passport_photo']
                coach.country = data['country']
                coach.region = data['region']
                coach.dob = data['dob']
                coach.gender = data['gender']
                coach.belt = data['belt']
                coach.level = data['coach_level']
                coach.contacts = data['contacts']
                coach.arrival_date = data['arrival_date']
                coach.departure_date = data['departure_date']
                coach.accommodation = data['accommodation']
                coach.save()

            # If the coach is also an athlete, link the athlete's coach field to themselves
            if athlete:
                athlete.coach = coach
                athlete.save()

        # If the person is only an athlete and not a coach, ensure the coach field is None
        elif athlete and not data.get('is_coach'):
            athlete.coach = None
            athlete.save()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    role_choices = [
        ('athlete', 'Athlete'),
        ('coach', 'Coach'),
        ('staff', 'Staff'),
        ('media', 'Media'),
    ]
    role = forms.ChoiceField(choices=role_choices, required=True, label="Register as")

    # Common fields
    passport_photo = forms.ImageField(required=False)
    name = forms.CharField(max_length=100, required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
    belt = forms.ModelChoiceField(queryset=Belt.objects.all(), required=False)
    id_passport_number = forms.CharField(max_length=50, required=False)
    dob = forms.DateField(required=False)
    gender = forms.CharField(max_length=10, required=False)
    contacts = forms.CharField(max_length=100, required=False)
    arrival_date = forms.DateField(required=False)
    accommodation = forms.CharField(max_length=100, required=False)
    
    # Role-specific fields
    level = forms.ChoiceField(choices=Coach.LEVEL_CHOICES, required=False)  # For Coach only
    role_field = forms.ModelChoiceField(queryset=Work.objects.all(), required=False)  # For Staff only
    media_house = forms.CharField(max_length=100, required=False)  # For Media only

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'passport_photo', 'name', 'country', 'belt', 'id_passport_number', 'dob', 'gender', 'contacts', 'arrival_date', 'accommodation', 'level', 'role_field', 'media_house']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        
        # Initially hide all role-specific fields
        self.fields['level'].widget = forms.HiddenInput()
        self.fields['role_field'].widget = forms.HiddenInput()
        self.fields['media_house'].widget = forms.HiddenInput()
        
        # Show fields based on selected role (if data is present)
        if 'role' in self.data:
            role = self.data.get('role')
            if role == 'athlete':
                self.fields['level'].widget = forms.HiddenInput()
                self.fields['role_field'].widget = forms.HiddenInput()
                self.fields['media_house'].widget = forms.HiddenInput()
            elif role == 'coach':
                self.fields['level'].widget = forms.Select()  # Show level field
                self.fields['role_field'].widget = forms.HiddenInput()
                self.fields['media_house'].widget = forms.HiddenInput()
            elif role == 'staff':
                self.fields['level'].widget = forms.HiddenInput()
                self.fields['role_field'].widget = forms.Select()  # Show role_field
                self.fields['media_house'].widget = forms.HiddenInput()
            elif role == 'media':
                self.fields['level'].widget = forms.HiddenInput()
                self.fields['role_field'].widget = forms.HiddenInput()
                self.fields['media_house'].widget = forms.TextInput() 

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class AthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = '__all__'

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = '__all__'

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'country', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter categories to include only team-related categories
        self.fields['category'].queryset = Category.objects.filter(
            name__in=['team_form', 'team_sparring', 'team_special_technique']
        )
class AthleteCategoryAssociationForm(forms.ModelForm):
    class Meta:
        model = AthleteCategoryAssociation
        fields = ['athlete', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter categories to include only individual-related categories
        self.fields['category'].queryset = Category.objects.filter(
            name__in=['individual_form', 'sparring', 'special_technique']
        )

class TeamMembershipForm(forms.ModelForm):
    class Meta:
        model = TeamMembership
        fields = '__all__'
