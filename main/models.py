import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.utils.text import slugify
from datetime import date

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

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('athlete', 'Athlete'),
        ('coach', 'Coach'),
        ('staff', 'Staff'),
        ('media', 'Media'),
        ('admin', 'Admin')
    ]
    
    LEVEL_CHOICES = [
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Other')
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='athlete')
    level = models.IntegerField(choices=LEVEL_CHOICES, default=4)

    def get_upload_path(self):
        if self.user_type == 'athlete':
            return 'athlete_photos/'
        elif self.user_type == 'coach':
            return 'coach_photos/'
        elif self.user_type == 'staff':
            return 'staff_photos/'
        elif self.user_type == 'media':
            return 'media_photos/'
        else:
            return 'default_photos/'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Additional logic to handle user-specific image processing or role setup

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Belt(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Work(models.Model):
    name = models.CharField(max_length=100, unique=True)
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

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='countries', default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='teams')
    
    def __str__(self):
        return f"{self.name} ({self.category})"

class AthleteCategoryAssociation(models.Model):
    athlete = models.ForeignKey('Athlete', on_delete=models.CASCADE, related_name='category_associations')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='athlete_associations')
    date_registered = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('athlete', 'category')
    
    def __str__(self):
        return f"{self.athlete.name} - {self.category.get_name_display()}"

class TeamMembership(models.Model):
    athlete = models.ForeignKey('Athlete', on_delete=models.CASCADE, related_name='team_memberships')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        unique_together = ('athlete', 'team')
    
    def __str__(self):
        return f"{self.athlete.name} in {self.team.name} ({self.team.category.get_name_display()})"

class Coach(models.Model):
    LEVEL_CHOICES = [
        ('Assistant', 'Assistant'),
        ('Head', 'Head'),
        ('Senior', 'Senior')
    ]
    
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    
    name = models.CharField(max_length=100, blank=True, null=True)
    passport_photo = models.ImageField(upload_to=upload_to)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='coaches')
    region = models.CharField(max_length=100, blank=True, null=True)
    id_number = models.CharField(max_length=50, unique=True)
    passport = models.CharField(max_length=50, unique=True)
    passport_date_of_issue = models.DateField()
    passport_place_of_issue = models.CharField(max_length=100)
    passport_expiry_date = models.DateField()
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    belt = models.ForeignKey(Belt, on_delete=models.CASCADE)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES)
    contacts = models.CharField(max_length=100)
    email = models.EmailField()
    arrival_date = models.DateField()
    departure_date = models.DateField(default=date.today)
    accommodation = models.CharField(max_length=100)

    def get_upload_path(self):
        return 'coach_photos/'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.passport_photo:
            image = process_image(self.passport_photo)
            image.save(self.passport_photo.path)

    def __str__(self):
        return self.name

class Athlete(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    
    name = models.CharField(max_length=100, blank=True, null=True)
    passport_photo = models.ImageField(upload_to=upload_to)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='athletes')
    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, related_name='athletes', blank=True, null=True, default=None)
    region = models.CharField(max_length=100, blank=True, null=True)
    id_passport_number = models.CharField(max_length=50, unique=True)
    passport = models.CharField(max_length=50, unique=True)
    passport_date_of_issue = models.DateField()
    passport_place_of_issue = models.CharField(max_length=100)
    passport_expiry_date = models.DateField()
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)  
    belt = models.ForeignKey(Belt, on_delete=models.CASCADE)
    contacts = models.CharField(max_length=100)
    email = models.EmailField()
    arrival_date = models.DateField()
    departure_date = models.DateField(default=date.today)
    accommodation = models.CharField(max_length=100)

    def get_upload_path(self):
        return 'athlete_photos/'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.passport_photo:
            image = process_image(self.passport_photo)
            image.save(self.passport_photo.path)

    
    
    @property
    def age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
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

    def __str__(self):
        return f"{self.name} ({self.gender}, {self.age}yrs, {self.weight}Kg)"      
class Staff(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]
    
    passport_photo = models.ImageField(upload_to=upload_to)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    id_passport_number = models.CharField(max_length=50, unique=True)
    role = models.ForeignKey(Work, on_delete=models.CASCADE)
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
