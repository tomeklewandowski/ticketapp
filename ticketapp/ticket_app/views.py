from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, AddEventForm
from django.views import View
from .models import Event


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
