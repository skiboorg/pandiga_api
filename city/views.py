from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import City
from rest_framework import generics

def create_city(request):
    from .cities import cities

    for i in cities:
        City.objects.create(city=i['city'],region=i['region'])
        print(i)


class SearchCity(generics.ListAPIView):
    serializer_class = CitiesSerializer

    def get_queryset(self):
        return City.objects.filter(city__startswith=self.request.query_params.get('city').capitalize())

class GetAllCities(generics.ListAPIView):
    queryset = City.objects.filter()
    serializer_class = CitiesSerializer