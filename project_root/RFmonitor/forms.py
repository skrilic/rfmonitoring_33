__author__ = 'slaven'

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

from django import forms

from base_stations.models import Profile


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'address')

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]