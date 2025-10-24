from main.models import User  # Replace 'MyUser' with the actual name of your custom user model
from main.models import Athlete

# Create a default user
default_user = User.objects.create(username='default_user')

# Assign the default user to existing athletes
athletes = Athlete.objects.filter(user_id__isnull=True)
for athlete in athletes:
    athlete.user = default_user
    athlete.save()
