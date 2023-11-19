from rest_framework import serializers
from .models import Place
from .models import LogEntry

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['place_name', 'x', 'y']

class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = '__all__'