from functools import reduce


from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .models import *
from .serializers import *
from notification.services import createNotification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notification.models import Notification

channel_layer = get_channel_layer()

class GetChat(generics.RetrieveAPIView):
    serializer_class = ChatSerializer
    def get_object(self):
        chat_id=self.request.query_params.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        return chat


class MessagesList(generics.ListAPIView):
    """Вывод сообщений в чате"""
    serializer_class = MessagesSerializer
    def get_queryset(self):
        chat_id=self.request.query_params.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
        messages = Message.objects.filter(chat=chat)

        unread_notifications = Notification.objects.filter(type='chat',user=self.request.user,chat_id=chat_id)
        unread_notifications.update(is_new=False)

        return messages

    # def get(self,request, chat_id):
    #     chat = Chat.objects.get(id=chat_id)
    #     messages = Message.objects.filter(chat=chat)
    #     serializer = MessagesSerializer(messages, many=True)
    #     return Response(serializer.data)

class ChatsList(generics.ListAPIView):
    """Вывод чатов"""
    serializer_class = ChatsSerializer
    def get_queryset(self):
        chat = Chat.objects.filter(users__in=[self.request.user.id]).order_by('-updatedAt')
        return chat

class SetChatRead(APIView):
    def post(self,request, chat_id):
        chat = Chat.objects.get(id=chat_id)
        messages = chat.messages
        chat.isNewMessages = False
        chat.save()
        messages.update(isUnread=False)
        return Response(status=200)


class ChatAdd(APIView):
    """Добавить сообщение в чат"""
    def post(self,request, chat_id):
        print('chat_id',chat_id)
        chat = Chat.objects.get(id=chat_id)
        new_message = Message.objects.create(chat=chat,
                               user=request.user,
                               message=request.data['message'])
        message = MessageSerializer(new_message,many=False)
        async_to_sync(channel_layer.group_send)('chat_%s' % chat.id,
                                                {"type": "chat.message", 'message': message.data})
        for user in chat.users.all():
            if user!= request.user:
                createNotification('chat', user, 'Новое сообщение в чате', '/lk/chats',chat_id=chat.id)


        return Response(status=201)

class ChatNewMessage(APIView):
    """Добавить сообщение в чат"""
    def post(self,request, owner_id):
        c = [request.user.id,owner_id]
        chats = Chat.objects.annotate(cnt=models.Count('users')).filter(cnt=len(c))
        chat_qs = reduce(lambda qs, pk: qs.filter(users=pk), c, chats)
        chat = None

        if len(chat_qs) == 0:
            chat = Chat.objects.create(starter=request.user,opponent_id=owner_id)
            chat.users.add(request.user.id)
            chat.users.add(owner_id)
        else:
            chat = chat_qs[0]
        print(request.data)
        msg_to = User.objects.get(id=owner_id)
        print(msg_to)
        createNotification('chat', msg_to, 'Новое сообщение в чате', '/lk/chats',chat_id=chat.id)
        # async_to_sync(channel_layer.send)(msg_to.channel, {"type": "user.notify"})
        if request.data['isRentMessage']:
            if request.data['rentType'] == 'true':
                Message.objects.create(chat=chat,
                                       user=request.user,
                                       isRentMessage=True,
                                       rentUnit_id=request.data['rentUnit'],
                                       rentType=True,
                                       rentDate=request.data['rentDate'],
                                       rentStartTime=request.data['rentTime'][0],
                                       rentEndTime=request.data['rentTime'][1],
                                       message='Привет!')
            if request.data['rentType'] == 'false':
                Message.objects.create(chat=chat,
                                       user=request.user,
                                       isRentMessage=True,
                                       rentUnit_id=request.data['rentUnit'],
                                       rentType=False,
                                       rentStartDate=request.data['rentDates'][0],
                                       rentEndDate=request.data['rentDates'][1],
                                       message='Привет!')
        else:
            Message.objects.create(chat=chat,
                                   user=request.user,
                                   message=request.data['message'])

        return Response(status=201)

