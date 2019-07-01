from rest_framework import serializers
from ticket_app.models import Event, Ticket


class EventSerializer(serializers.ModelSerializer):
    event = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='event')

    class Meta:
        model = Event
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    ticket = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='ticket')

    class Meta:
        model = Ticket
        fields = '__all__'
