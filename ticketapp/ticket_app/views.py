import datetime
from background_task import background
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from ticket_app.forms import AddEventForm
from django.views import View
from .models import Event, Ticket
from ticket_app.serializers import EventSerializer, TicketSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import viewsets
from django.core.serializers import json


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

    def get(self, event, request, format=None):
        self.get = json.dumps(event)


class EventListViewSet(viewsets.ModelViewSet):

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer_class = EventSerializer(events, many=True, context={"request": request})
        return Response(serializer_class.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, serializer, request, format=None):
        self.get = json.dumps(serializer)



class EventViewSet(viewsets.ModelViewSet):

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        event = self.get_object(id)
        serializer_class = EventSerializer(event, context={"request": request})
        return Response(serializer_class.data)

    def delete(self, id, request, format=None):
        event = self.get_object(id)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, id, format=None):
        event = self.get_object(id)
        serializer_class = EventSerializer(event, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, id, format=None):
        pass

    def get(self, event, request, format=None):
        self.get = json.dumps(event)


class AvailableTicketsViewSet(APIView):

    def get_event_tickets(self, pk):
        try:
            e = Event.objects.get(pk=pk)
            types = e.ticket_types
            resp = dict()
            for ticket_type in types:
                queryset = Ticket.objects.filter(reservation_status=1, event=Event.id).count()
                resp.add(ticket_type, queryset)
            return resp
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, event_id):
        return Response(self.get_event_tickets(event_id))


class ReservationViewSet(APIView):

    def reserve_ticket(self, event_id, ticket_type):
        ticket = Ticket.objects.filter(id=int(event_id), ticket_type=int(ticket_type), reservation_status='1').first()
        ticket.reservation_status=2
        ticket.reservation_date=datetime.now()
        ticket.save()
        self.expire(ticket.id)
        return Response(ticket.id, ticket.price)

    def get(self, request, event_id, ticket_type):
        return Response(self.reserve_ticket(event_id, ticket_type))

    @background(schedule=15*60)
    def expire(self, ticket_id):
        queryset = Ticket.objects.get(pk=ticket_id)
        queryset.reservation_status=1
        queryset.save()


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class TicketPayViewSet(viewsets.ModelViewSet):

    def ticket_payment(self, request, event_id, ticket_type, reservation_date, price, format=None):
        queryset = Ticket.objects.filter(id=int(event_id), ticket_type=int(ticket_type), reservation_status=2, reservation_date=reservation_date, price=price)
        #verify_cash_amount = it belongs to an external api or maybe a django-paypal
        #also need to check is payment is equl to price of ticket
        verify_cash_amount = True
        if verify_cash_amount is True:
            queryset.reservation_status=3
            queryset.reservation_date=datetime.now()
            queryset.save()
        else:
            HttpResponse(f'Please pay your ticket')
            return Response(queryset)

    def get(self, queryset, request, format=None):
        self.get = json.dumps(queryset)


class Stats(APIView):

    def get(self, request):
        result = dict()
        tickets_count = Ticket.objects.all().count()
        result['total_tickets'] = tickets_count
        ticket_reserved = Ticket.objects.filter(reservation_status='1').count()
        result['reserve_tickets'] = ticket_reserved
        # and so on
        return Response(result)


#Maybe this would help but I have not enough time

# from django.urls import reverse
# from django.shortcuts import render
# from paypal.standard.forms import PayPalPaymentsForm
#
#
# def view_that_asks_for_money(request):
#
#     paypal_dict = {
#         "business": "receiver_email@example.com",
#         "amount": "10000000.00",
#         "item_name": "name of the item",
#         "invoice": "unique-invoice-id",
#         "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
#         "return": request.build_absolute_uri(reverse('your-return-view')),
#         "cancel_return": request.build_absolute_uri(reverse('your-cancel-view')),
#         "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
#     }
#
#     form = PayPalPaymentsForm(initial=paypal_dict)
#     context = {"form": form}
#     return render(request, "payment.html", context)





