import datetime
from background_task import background
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from . forms import AddEventForm
from django.views import View
from .models import Event, Ticket
from ticket_app.serializers import EventSerializer, TicketSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class AddEventView(View):
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


class EventList(APIView):

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventView(APIView):

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        event = self.get_object(id)
        serializer = EventSerializer(event, context={"request": request})
        return Response(serializer.data)

    def delete(self, request, id, format=None):
        event = self.get_object(id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id, format=None):
        event = self.get_object(id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id, format=None):
        pass


class AvailableTickets(APIView):

    def get_event_tickets(self, pk, request, format=None):
        try:
            e = Event.objects.get(pk=pk)
            types = e.ticket_types
            resp = dict()
            for ticket_type in types:
                count_of_tickets = Entry.objects.filter(reservation_status=1, event=Event.id, ticket_type=ticket_type).count()
                resp.add(ticket_type, count_of_tickets)
            return resp
        except Event.DoesNotExist:
            raise Http404

    def get(self, resp, request, format=None):
        self.get = json.dumps(resp)


class Reservation(APIView):

    def get_available_ticket(self, request, event_id, ticket_type, format=None):
        reserved_ticket = Ticket.objects.filter(id=int(event_id), ticket_type=int(ticket_type), reservation_status=1).first()
        reserved_ticket.reservation_status=2
        reserved_ticket.reservation_date=datetime.now()
        reserved_ticket.save()
        self.expire(reserved_ticket.id)
        return Response(reserved_ticket.id, price)

    @background(schedule=15*60)
    def expire(self, ticket_id):
        reserved_ticket = Ticket.objects.get(pk=ticket_id)
        reserved_ticket.reservation_status=1
        reserved_ticket.save()









