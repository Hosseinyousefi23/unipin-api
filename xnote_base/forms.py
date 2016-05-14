from django import forms
from xnote_base.models import Group


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['related_university', 'real_name', 'description', 'url_name', 'profile_image']
