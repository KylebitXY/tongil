from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from main1.models import Tournament, Coach, Athlete, TournamentParticipation
from .forms import AthleteSelectionForm
from django.urls import reverse

@login_required
def register_athletes(request, tournament_id, coach_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    coach = get_object_or_404(Coach, id=coach_id)

    if request.method == 'POST':
        form = AthleteSelectionForm(request.POST, tournament=tournament)
        if form.is_valid():
            selected_athletes = form.cleaned_data['athletes']
            for athlete in selected_athletes:
                # Check if the athlete is already participating in the tournament
                if not TournamentParticipation.objects.filter(
                    tournament=tournament,
                    coach=coach,
                    athlete=athlete
                ).exists():
                    TournamentParticipation.objects.create(
                        tournament=tournament,
                        coach=coach,
                        athlete=athlete
                    )
            return redirect(reverse('success_page'))  # Redirect to a success page or list of athletes
    else:
        form = AthleteSelectionForm(tournament=tournament)

    context = {
        'form': form,
        'tournament': tournament,
        'coach': coach,
    }

    return render(request, 'client/register_athletes.html', context)
