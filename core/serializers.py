from .models import *
from rest_framework.serializers import ModelSerializer

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 'location', 'attendees', 'recurrence']

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'timezone']