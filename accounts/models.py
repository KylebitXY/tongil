from django.contrib.auth.models import User
from main1.models import Coach

def link_user_to_coach(user_id, coach_id):
    try:
        user = User.objects.get(id=user_id)
        coach = Coach.objects.get(id=coach_id)
        
        # Assuming some sort of linking logic
        # This example assumes that the coach's name should be used to update the user's details
        # Replace this logic with the actual linking you need

        # Example: Set the user's first and last name based on coach's name
        user.first_name = coach.name.split(' ')[0]
        user.last_name = ' '.join(coach.name.split(' ')[1:])
        user.save()

        print(f"Linked Coach {coach.name} to User {user.username}")

    except User.DoesNotExist:
        print(f"User with id {user_id} does not exist.")
    except Coach.DoesNotExist:
        print(f"Coach with id {coach_id} does not exist.")


#from accounts.models import link_user_to_coach
#link_user_to_coach(user_id=3, coach_id=6)