from django import forms
from .models import Article, Schedule


class ArtForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ['status', 'generaluser']


class ScheduleForm(forms.ModelForm):

    class Meta:
        model = Schedule
        exclude = ["Article"]
