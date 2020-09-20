import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .serializers import *

class NotificationSetRead(APIView):
    def post(self,request):
        notify = Notification.objects.filter(user=request.user, is_new=True).order_by('-created_at')
        notify.update(is_new=False)
        return Response(status=200)

class NotificationGet(generics.ListAPIView):
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        user = self.request.user
        notify = Notification.objects.filter(user=user,is_new=True).order_by('-created_at')
        return notify

class NotificationGetAll(generics.ListAPIView):
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        user = self.request.user
        notify = Notification.objects.filter(user=user).order_by('-created_at')
        return notify