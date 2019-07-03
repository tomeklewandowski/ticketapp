from django.test import TestCase
from ticket_app.models import Event
from rest_framework.test import APIClient


class EventTestCase(TestCase):
    def setUp(self):
        Event.objects.create(name="Juwenalia", date="2019-05-11", types="[youth]")
        Event.objects.create(name="Wesele Figara", date="2019-06-12", types="[bride]")

    def test_events_in_db(self):

        client = APIClient()
        output = client.get('/api/list_events/', format='json')
        print(output)