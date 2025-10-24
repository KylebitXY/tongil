from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from main1.models import Athlete, Coach

class UserRegistrationForm(forms.ModelForm):
    USER_TYPE_CHOICES = (
        ('athlete', 'Athlete'),
        ('coach', 'Coach'),
    )
    
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User  # We're now creating a User instance directly
        fields = ['username', 'password', 'confirm_password', 'user_type']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        # Determine the user type and create corresponding profile
        user_type = self.cleaned_data['user_type']
        if user_type == 'athlete':
            Athlete.objects.create(user=user, name=user.username)
        elif user_type == 'coach':
            Coach.objects.create(user=user, name=user.username)

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
