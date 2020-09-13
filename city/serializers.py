from rest_framework import serializers
from .models import *


class CitiesSerializer(serializers.ModelSerializer):
    """Список городов"""
    class Meta:
        model = City
        fields = ['id', 'city', 'region', 'coefficient']


class CitySerializer(serializers.ModelSerializer):
    """Список городов"""
    class Meta:
        model = City
        fields = '__all__'