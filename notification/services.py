from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
def createNotification(type,user,text,url):
    Notification.objects.create(
        type=type,
        user=user,
        text=text,
        url=url)
    try:
        async_to_sync(channel_layer.send)(user.channel, {"type": "user.notify",
                                                         'event':type,
                                                         'message':text,
                                                         'url':url})
    except:
        print('user offline')