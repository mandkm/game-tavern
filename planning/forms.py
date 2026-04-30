from django import forms
from .models import Participation
from games.models import GameCategory
from food.models import Food

class ParticipationForm(forms.ModelForm):
    class Meta:
        model = Participation
        fields = ['available', 'alternative_date', 'can_host', 'food', 'game_category']
        widgets = {
            'alternative_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'game_category': forms.CheckboxSelectMultiple(),
        }
        labels = {
            'available': 'Ich kann teilnehmen',
            'alternative_date': 'Alternativtermin (optional)',
            'can_host': 'Ich kann hosten',
            'food': 'Essen',
            'game_category': 'Spielstimmung diese Woche',
        }
