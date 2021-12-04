from django import forms
from officemanagement.models import Office, Schedule, GeneralUserOffice


class OfficeForm(forms.ModelForm):
    class Meta:
        model = Office
        exclude = ['status', 'admin']


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        exclude = ["office"]


class ScoreForm(forms.ModelForm):
    class Meta:
        model = GeneralUserOffice
        fields = ["generaluser", "office", "scores", "comments"]

    generaluser = forms.CharField(label="用户", disabled=True)
    # office = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    office = forms.CharField(label="会议室", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['generaluser'] = self.instance.generaluser
        self.initial['office'] = self.instance.office

    def clean_generaluser(self):
        return self.initial['generaluser']

    def clean_office(self):
        return self.initial['office']


class RateForm(forms.ModelForm):
    class Meta:
        model = GeneralUserOffice
        fields = ["office", "scores", "comments", "rating", "assessment"]

    generaluser = forms.CharField(label="会议室", disabled=True)
    scores = forms.IntegerField(label="得分", disabled=True)
    comments = forms.CharField(label="会议室评价", disabled=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['office'] = self.instance.office
        self.initial['scores'] = self.instance.scores
        self.initial['comments'] = self.instance.comments

    def clean_office(self):
        return self.initial['office']

    def clean_scores(self):
        return self.initial['scores']

    def clean_comments(self):
        return self.initial['comments']
