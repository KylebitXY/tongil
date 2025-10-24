from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main1.models import Coach, Athlete

@login_required
def index_view(request):
    # Check if the user is a coach
    if Coach.objects.filter(user=request.user).exists():
        # Get the coach object for the logged-in user
        coach = Coach.objects.get(user=request.user)
        region_name = coach.region.name if coach.region else "N/A"

        # Calculate totals relevant to the coach
        total_athletes = Athlete.objects.filter(coach=coach).count()  # Athletes assigned to this coach
        total_females = Athlete.objects.filter(coach=coach, gender='Female').count()  # Athletes assigned to this coach
        total_males = Athlete.objects.filter(coach=coach, gender='Male').count()
        overall_total = total_males + total_females

        # Pass coach-specific data to the template
        context = {
            'coach': coach,
            'total_athletes': total_athletes,
            'total_females': total_females,
            'total_males': total_males,
            'overall_total': overall_total,
            'region_name': region_name,
            # You can add more coach-specific data here if needed
        }
        
        # Render the coach dashboard template with coach-specific context
        return render(request, 'index1.html', context)
    else:
        # Calculate totals for the admin dashboard
        total_males = (Coach.objects.filter(gender='Male').count() + 
                       Athlete.objects.filter(gender='Male').count())

        total_females = (Coach.objects.filter(gender='Female').count() + 
                         Athlete.objects.filter(gender='Female').count())

        total_coaches = Coach.objects.count()

        # Include coaches who are also athletes in the athlete tally
        total_athletes = (Athlete.objects.count() + 
                          Coach.objects.filter(is_athlete=True).count())
        total_athletes2 = Athlete.objects.count()
        overall_total = total_coaches + total_athletes2

        total_countries = Athlete.objects.values('country').distinct().count()

        # Pass totals to the template
        context = {
            'total_males': total_males,
            'total_females': total_females,
            'total_coaches': total_coaches,
            'total_athletes': total_athletes,
            'overall_total': overall_total,
            'total_countries': total_countries,
        }

        # Render the admin dashboard template with context
        return render(request, 'index.html', context)

@login_required
def coach_dashboard(request):
    try:
        # Get the coach associated with the logged-in user
        coach = Coach.objects.get(user=request.user)
        
        # Filter active athletes for the coach
        active_athletes = Athlete.objects.filter(coach=coach, is_active=True)
        
        # Prepare context with relevant data
        context = {
            'active_athletes': active_athletes,
            'coach': coach,
        }
        
        # Render the coach dashboard template
        return render(request, 'index1.html', context)
    
    except Coach.DoesNotExist:
        # Handle the case where no coach is found for the logged-in user
        return render(request, 'no_coach.html', {'message': 'You are not assigned as a coach.'})
