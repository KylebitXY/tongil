from django import forms
from main1.models import Athlete, Tournament, TournamentParticipation

class AthleteSelectionForm(forms.Form):
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        tournament = kwargs.pop('tournament')
        super().__init__(*args, **kwargs)
        self.fields['athletes'].queryset = Athlete.objects.exclude(
            tournamentparticipation__tournament=tournament
        )
