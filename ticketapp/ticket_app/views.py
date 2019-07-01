from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from . forms import LoginForm, AddEventForm
from django.views import View
from rest_framework import generics
from .models import Event, Ticket
from showtimes.serializers import EventSerializer, TicketSerializer


class MainView(View):
    def get(self, request):
        ctx = {"event": Event}
        return render(request, "base.html", ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return HttpResponse("You are not log in, so you can't add new event.")


def logout_view(request):
    logout(request)
    return redirect('/')


class AddEventView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddEventForm()
        return render(request, "addevent.html", {"form": form})

    def post(self, request):
        form = AddEventForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            date = form.cleaned_data.get('date')
            types = form.cleaned_data.get('types')
            event = Event(name=name,
                          date=date,
                          types=types,
                          )
            try:
                event.save()
            except IntegrityError:
                return HttpResponse('This event is already here.')
            ctx = {"event": event}
            return render(request, "new_event.html", ctx)


class EventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.filter()
    serializer_class = EventSerializer


class TicketScreeningListView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.filter()
    serializer_class = TicketSerializer


