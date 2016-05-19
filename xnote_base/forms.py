from django import forms
from django.core.exceptions import ValidationError
from xnote_base.models import Group


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean_username(self):
        if self.cleaned_data['username'] == 'ez':
            raise ValidationError('you are too ez to login, go next')

        return self.cleaned_data['username']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['related_university', 'real_name', 'description', 'url_name', 'profile_image']
