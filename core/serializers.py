from .models import *
from rest_framework.serializers import ModelSerializer

class EventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'timezone']