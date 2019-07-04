from django.test import TestCase
from ticket_app.models import Event, Ticket
from rest_framework.test import APIClient


class EventTestCase(TestCase):
    def setUp(self):
        Event.objects.create(name="Juwenalia", date="2019-05-11", types="[youth]")
        Event.objects.create(name="Wesele Figara", date="2019-06-12", types="[bride]")

    def test_events_in_db(self):

        client = APIClient()
        output = client.get('/api/list_events/', format='json')
        print(output)


class TicketTestCase(TestCase):
    def setUp(self):
        Ticket.objects.create(price="50", ticket_type="1", reservation_date="2019-05-11", reservation_status="1", event=Event)
        Ticket.objects.create(price="100", ticket_type="4", reservation_date="2019-06-12", reservation_status="3", event=Event)

    def test_tickets_in_db(self):

        client = APIClient()
        output = client.get('/available_tickets/<int:event_id>/', format='json')
        print(output)