from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    party_affiliation = forms.CharField(required=False)
    min_birth = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1900, 2025)))
    max_birth = forms.DateField(required=False, widget=forms.SelectDateWidget(years=range(1900, 2025)))
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + [(i, i) for i in range(6)], required=False)

    v20state = forms.BooleanField(required=False)
    v21town = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town = forms.BooleanField(required=False)

