import json
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from .serializers import *
import settings
from pyfcm import FCMNotification


class NotificationGetOtherCount(APIView):
    def get(self,request):
        notify = Notification.objects.filter(user=request.user, is_new=True, type='order').order_by('-created_at')
        return Response({'new_messages': notify.count()}, status=200)

class NotificationGetMessagesCount(APIView):
    def get(self,request):
        # push_service = FCMNotification(api_key=settings.FCM_API_KEY)
        # registration_id = 'dT7bZ94aSPWr4_XXrisXso:APA91bHhzZH8CMLZbpdaERXnRVneFmbJwOdPe-tgZiNcaeoP54KJlhoSV86kjOs-iQUmDCmg2WIPeotqmwFln3hI-tv1imBWa8q5-lUfgR9kb3ecKHHVg7nDel1kpqmVsf7Kp7NI-0T5'
        # message_title = "Uber update"
        # message_body = "Hi john, your customized news for today is ready"
        # data_message = {
        #     "Nick": "Mario",
        #     "body": "great match!",
        #     "Room": "PortugalVSDenmark",
        #     "url": "/profile/"
        #
        # }
        # extra_notification_kwargs={
        #     "url": "/profile/",
        # }
        #
        # result = push_service.notify_single_device(registration_id=registration_id,
        #                                            sound='Default',
        #                                            message_title=message_title,
        #                                            message_body=message_body,
        #                                            data_message=data_message,
        #                                            extra_notification_kwargs=extra_notification_kwargs)
        # print(result)
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
        print(request.data)
        notify = Notification.objects.get(user=request.user, id=request.data['id'])
        notify.is_new=False
        notify.save()
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