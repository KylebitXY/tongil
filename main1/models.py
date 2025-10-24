import os
from django.db import models
from django.utils.text import slugify
from datetime import date
from PIL import Image
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.auth.models import User

# Helper Functions
def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.name)}.{ext}"
    return os.path.join(instance.get_upload_path(), filename)

def process_image(image, target_size=(413, 531)):
    img = Image.open(image)
    img = img.convert("RGB")
    img.thumbnail(target_size, Image.LANCZOS)
    thumb = Image.new('RGB', target_size, (255, 255, 255))
    img_position = (
        (target_size[0] - img.size[0]) // 2,
        (target_size[1] - img.size[1]) // 2
    )
    thumb.paste(img, img_position)
    return thumb

# Models
class Country(models.Model):
    name = models.CharField(max_length=100)
    joined_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class Belt(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    joined_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('individual_form', 'Individual Form'),
        ('team_form', 'Team Form'),
        ('sparring', 'Sparring'),
        ('team_sparring', 'Team Sparring'),
        ('special_technique', 'Special Technique'),
        ('team_special_technique', 'Team Special Technique')
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()

class RoleType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Club(models.Model):
    name = models.CharField(max_length=100)
    county = models.CharField(max_length=100, blank=True, null=True)
    joined_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.county})"

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    edition = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return format_html(
            '{} {}<sup>{}</sup> - Edition',
            self.name,
            self.edition,
            self.get_ordinal_suffix(self.edition)
        )
    
    def get_ordinal_suffix(self, number):
        """Return the ordinal suffix for a given number."""
        if 10 <= number % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
        return suffix
class BaseProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    passport_photo = models.ImageField(upload_to=upload_to, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='%(class)s_profiles')
    region = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='%(class)s_region', blank=True, null=True)
    id_passport_number = models.CharField(max_length=50, blank=True, null=True )
    passport = models.CharField(max_length=50, null=True, blank=True)
    passport_date_of_issue = models.DateField(blank=True, null=True)
    passport_place_of_issue = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True, related_name='%(class)s_passports')
    passport_expiry_date = models.DateField(blank=True, null=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    email = models.EmailField(blank=True, null=True)
    contacts = models.CharField(max_length=100, blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default='O+', blank=True, null=True)
    arrival_date = models.DateField(blank=True, null=True)
    departure_date = models.DateField(default=date.today, blank=True, null=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='%(class)s_accommodation', blank=True, null=True)
    joined_date = models.DateField(default=timezone.now)
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.country.name == "Kenya" and not self.region:
            self.region = self.country.name  # or handle explicitly if required

        super().save(*args, **kwargs)

        # Process and save the passport photo
        if self.passport_photo:
            image = process_image(self.passport_photo)
            image.save(self.passport_photo.path)

    @property
    def age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age

    def __str__(self):
        return self.name
    
    @property
    def get_weight_category(self):
        if self.gender.lower() == 'male':
            if 18 <= self.age <= 35:
                if self.weight <= 54.9:
                    return 'Fin Weight Division'
                elif 55 <= self.weight <= 59.9:
                    return 'Fly Weight Division'
                elif 60 <= self.weight <= 64.9:
                    return 'Bantam Weight Division'
                elif 65 <= self.weight <= 69.9:
                    return 'Feather Weight Division'
                elif 70 <= self.weight <= 74.9:
                    return 'Light Weight Division'
                elif 75 <= self.weight <= 79.9:
                    return 'Welter Weight Division'
                elif 80 <= self.weight <= 84.9:
                    return 'Middle Weight Division'
                elif 85 <= self.weight <= 89.9:
                    return 'Heavy Weight Division'
                elif 90 <= self.weight <= 100:
                    return 'Super Heavy Weight Division'
                elif self.weight > 100:
                    return 'Super Heavy Weight Division Level 1'
            elif 36 <= self.age <= 49:
                if 50.9 <= self.weight <= 59.9:
                    return 'Fly Weight Division'
                elif 60 <= self.weight <= 69.9:
                    return 'Middle Weight Division'
                elif 70 <= self.weight <= 79.9:
                    return 'Heavy Weight Division'
                elif 80 <= self.weight <= 89.9:
                    return 'Super Heavy Weight Division'
                elif self.weight >= 90:
                    return 'Super Heavy Weight Division Level 0'
        elif self.gender.lower() == 'female':
            if 18 <= self.age <= 49:
                if 50.9 <= self.weight <= 59.9:
                    return 'Fly Weight Division'
                elif 60 <= self.weight <= 69.9:
                    return 'Middle Weight Division'
                elif 70 <= self.weight <= 79.9:
                    return 'Heavy Weight Division'
                elif 80 <= self.weight <= 89.9:
                    return 'Super Heavy Weight Division'
                elif self.weight >= 90:
                    return 'Super Heavy Weight Division Level 0'
        return 'Unknown Category'

class Coach(BaseProfile):
    LEVEL_CHOICES = [
        ('Assistant', 'Assistant'),
        ('Head', 'Head'),
        ('Senior', 'Senior'),
    ]
    is_athlete = models.BooleanField(default=False)  # New field
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, blank=True, null=True)
    belt = models.ForeignKey(Belt, on_delete=models.CASCADE, related_name='coach_belt', blank=True, null=True)

    # Athlete-specific fields
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    category = models.ManyToManyField(Category, blank=True, related_name='coach_category')
   

    def get_upload_path(self):
        return 'coach_photos/'

    def __str__(self):
        return f"{self.name} - Coach{' & Athlete' if self.is_athlete else ''}"
        
    
    
class Athlete(BaseProfile):
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    category = models.ManyToManyField(Category, blank=True, related_name='athlete_associations')
    belt = models.ForeignKey(Belt, on_delete=models.CASCADE, related_name='athlete_belt', blank=True, null=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='athlete_coach', blank=True, null=True)
    teams = models.ManyToManyField('Team', related_name='athletes', blank=True)
    is_active = models.BooleanField(default=True)  # Add this field


    def get_upload_path(self):
        return 'athlete_photos/'

  

    def __str__(self):
        return f"{self.name} - Athlete"

class TournamentParticipation(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, blank=True, null=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    performance = models.CharField(max_length=255, blank=True, null=True)  # Performance details


    def __str__(self):
        return f"{self.tournament} - {self.coach or self.athlete} - {self.category}"



class Team(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='teams', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='teams', blank=True, null=True)
    members = models.ManyToManyField('Athlete', related_name='team_members', blank=True)

    def __str__(self):
        return self.name

class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='memberships')
    joined_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.athlete.name} in {self.team.name}"

class Staff(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    ROLE_CHOICES = [
        ('Photographer', 'Photographer'),
        ('Handy man', 'Handy man'),
        ('Security', 'security'),
        ('Driver', 'driver'),
        ('Technitian ', 'Technitian'),
        ('Water dist', 'Water dist')
    ]
    passport_photo = models.ImageField(upload_to=upload_to)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    id_passport_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    contacts = models.CharField(max_length=100)

    def get_upload_path(self):
        return 'staff_photos/'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.passport_photo:
            image = process_image(self.passport_photo)
            image.save(self.passport_photo.path)

    def __str__(self):
        return self.name

class Media(models.Model):
    ROLE_CHOICES = [
        ('Photographer', 'Photographer'),
        ('Journalist', 'Journalist'),
        ('Videographer', 'Videographer')
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    
    passport_photo = models.ImageField(upload_to=upload_to)
    name = models.CharField(max_length=100)
    id_passport_number = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    contacts = models.CharField(max_length=100)
    media_house = models.CharField(max_length=100)

    def get_upload_path(self):
        return 'media_photos/'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.passport_photo:
            image = process_image(self.passport_photo)
            image.save(self.passport_photo.path)

    def __str__(self):
        return self.name
