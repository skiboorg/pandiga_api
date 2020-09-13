from rest_framework import exceptions, serializers
from user.serializers import UserSerializer

from .models import *

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

