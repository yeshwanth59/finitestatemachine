from django import forms
from statemachine.models import User


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {"pwd": forms.PasswordInput()}
        fields = ["name", "mobileNo", "email", "pwd"]


class LoginForm(forms.Form):
    email = forms.CharField(max_length=41)
    pwd = forms.CharField(widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {"pwd": forms.PasswordInput()}
        fields = ["name", "mobileNo", "email", "pwd"]
