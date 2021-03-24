import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .serializers import *

class NotificationGetOtherCount(APIView):
    def get(self,request):
        notify = Notification.objects.filter(user=request.user, is_new=True, type='order').order_by('-created_at')
        return Response({'new_messages': notify.count()}, status=200)

class NotificationGetMessagesCount(APIView):
    def get(self,request):
        notify = Notification.objects.filter(user=request.user, is_new=True, type='chat').order_by('-created_at')
        return Response({'new_messages': notify.count()}, status=200)

class NotificationDelete(APIView):
    def post(self, request):
        data = request.data
        notify = Notification.objects.get(id=data.get('id'))
        notify.delete()
        print(data)
        return Response(status=200)
class NotificationSetRead(APIView):
    def post(self,request):
        notify = Notification.objects.filter(user=request.user, is_new=True).order_by('-created_at')
        notify.update(is_new=False)
        return Response(status=200)

class NotificationGet(generics.ListAPIView):
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        user = self.request.user
        notify = Notification.objects.filter(user=user,type='order').order_by('-created_at')
        return notify

class NotificationGetAll(generics.ListAPIView):
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        user = self.request.user
        notify = Notification.objects.filter(user=user,type='order').order_by('-created_at')
        return notify