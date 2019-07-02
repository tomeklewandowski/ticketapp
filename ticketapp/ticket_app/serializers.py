from rest_framework import serializers
from ticket_app.models import Event, Ticket


class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class TicketSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'
