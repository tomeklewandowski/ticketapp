from django import forms
from . models import Event, Ticket
from django.forms import ModelForm
from .models import ticketsType, reservationStatus


class LoginForm (forms.Form):
    username = forms.CharField(label="Login", strip=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class AddEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = "__all__"


class BuyTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = "__all__"