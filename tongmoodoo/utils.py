from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

def send_coach_registration_link(coach, tournament):
    # Generate a unique registration link
    registration_link = reverse('register_athletes', args=[tournament.id, coach.id])
    
    # Email details
    subject = 'Tournament Athlete Registration'
    message = f"""
    Dear {coach.name},
    
    The registration for the upcoming tournament '{tournament.name}' has begun.
    Please use the following link to register your athletes or update their details:
    {settings.SITE_URL}{registration_link}
    
    Best regards,
    The Tournament Team
    """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [coach.email])
