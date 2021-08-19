from django import forms
from defaultAPP.models import GeneralUser, Admin


class GeneralUserLoginForm(forms.Form):
    uid = forms.CharField(label='编号', max_length=10)
    password = forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)


class AdminLoginForm(forms.Form):
    uid = forms.CharField(label='编号', max_length=10)
    password = forms.CharField(label='密码', max_length=30, widget=forms.PasswordInput)

class GeneralUserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = GeneralUser
        fields = ('no',
                  'name',
                  'password',
                  'confirm_password',
                  'gender',
                  'birthday',
                  'email',
                  'info')

    def clean(self):
        cleaned_data = super(GeneralUserRegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match.')


class AdminRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = Admin
        fields = ('name',
                  'password',
                  'confirm_password',
                  'gender',
                  'birthday',
                  'email',
                  'info')

    def clean(self):
        cleaned_data = super(AdminRegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if confirm_password != password:
            self.add_error('confirm_password', 'Password does not match.')

class GeneralUserUpdateForm(GeneralUserRegisterForm):
    class Meta:
        model = GeneralUser
        fields = ('name',
                  'password',
                  'confirm_password',
                  'gender',
                  'birthday',
                  'email',
                  'info')