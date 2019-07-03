from django.core.serializers import json
from django.db import models


ticketsType = (
    ("1", "Regular"),
    ("2", "Premium"),
    ("3", "VIP"),
    ("4", "Reduced"),
)

reservationStatus = (
    ("1", "Available"),
    ("2", "Reserved"),
    ("3", "Paid"),
)


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, default="Event")
    date = models.DateTimeField(null=True)
    types = models.TextField(default=None, null=True)

    def set_types(self, types_list):
        self.set_types = json.dumps(types_list)

    def get_types(self):
        return json.loads(self.set_types)


class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(decimal_places=2, max_digits=15, default=0)
    ticket_type = models.IntegerField(choices=ticketsType)
    reservation_date = models.DateTimeField(auto_now_add=True)
    reservation_status = models.IntegerField(choices=reservationStatus, default=1)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

