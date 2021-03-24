from rest_framework import exceptions, serializers
from djoser.conf import settings
from .models import *
from user.serializers import UserSerializer,UserSerializerTemp
from technique.serializers import TechniqueUnitSerializer


class ChatSerializer(serializers.ModelSerializer):
    starter = UserSerializer()
    opponent = UserSerializer()
    class Meta:
        model = Chat
        fields = [
            'id',
            'isNewMessages',
            'updatedAt',
            'starter',
            'opponent',

            ]

class ChatsSerializer(serializers.ModelSerializer):
    starter = UserSerializer()
    opponent = UserSerializer()
    last_message = serializers.CharField(source='get_last_message_text')
    last_message_user_id = serializers.CharField(source='get_last_message_user_id')
    last_message_user_name = serializers.CharField(source='get_last_message_user_name')
    last_message_user_status = serializers.BooleanField(source='get_last_message_user_status')
    last_message_user_avatar = serializers.CharField(source='get_last_message_user_avatar')
    class Meta:
        model = Chat
        fields = [
            'id',
            'isNewMessages',
            'updatedAt',
            'starter',
            'opponent',
            'last_message',
            'last_message_user_id',
            'last_message_user_avatar',
            'last_message_user_name',
            'last_message_user_status']

class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializerTemp()
    class Meta:
        model = Message
        fields = [
            'id',
            'chat',
            'user',
            'message',
            'createdAt']

class MessagesSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    rentUnit = TechniqueUnitSerializer()
    
    class Meta:
        model = Message
        fields = [
            'id',
            'user',
            'message',
            'isUnread',
            'isRentMessage',
            'rentUnit',
            'rentType',
            'rentDate',
            'rentDays',
            'rentTime',
            'rentHours',
            'createdAt',
            'chat']