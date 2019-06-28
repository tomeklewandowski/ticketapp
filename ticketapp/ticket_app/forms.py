from django import forms
from django.core.validators import EmailValidator
from. models import Event, Ticket
from django.forms import ModelForm
from .models import ticketsType, reservationStatus


class LoginForm (forms.Form):
    username = forms.CharField(label="Login", strip=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class UserDataForm(forms.Form):
    first_name = forms.CharField(label="Name", max_length=100)
    last_name = forms.CharField(label="Surname", max_length=100)
    email = forms.CharField(label="mail", max_length=100, validators=[EmailValidator()])


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, strip=True, label="Please enter your login")
    password = forms.CharField(label="Enter password", widget=forms.PasswordInput)
    password_again = forms.CharField(label="Password again", widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=50, strip=True, label="Enter your name")
    last_name = forms.CharField(max_length=50, strip=True, label="Enter your surname")
    email = forms.EmailField(max_length=50, label="Enter your email")

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")

        if password != password_again:
            raise forms.ValidationError(
                "password and password_again does not match")


class AddEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['name', 'date', 'types']