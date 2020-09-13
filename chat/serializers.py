from rest_framework import exceptions, serializers
from djoser.conf import settings
from .models import *
from user.serializers import UserSerializer
from technique.serializers import TechniqueUnitSerializer
class ChatsSerializer(serializers.ModelSerializer):

    last_message = serializers.CharField(source='get_last_message_text')
    last_message_user_id = serializers.CharField(source='get_last_message_user_id')
    last_message_user_name = serializers.CharField(source='get_last_message_user_name')
    last_message_user_avatar = serializers.CharField(source='get_last_message_user_avatar')
    class Meta:
        model = Chat
        fields = [
            'id',
            'isNewMessages',
            'updatedAt',
            'last_message',
            'last_message_user_id',
            'last_message_user_avatar',
            'last_message_user_name'
                  ]

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
            'rentStartDate',
            'rentEndDate',
            'rentStartTime',
            'rentEndTime',
            'createdAt',
                  ]