from django import forms
from .models import TeamDetail


class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamDetail
        fields = ('leader_name', 'leader_email', 'leader_mobile', 'member2_name', 'member2_email', 'member3_name', 'member3_email')