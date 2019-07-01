from django import forms
from . models import Event, Ticket


class AddEventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = "__all__"


class BuyTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = "__all__"

