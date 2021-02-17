from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from django.template.loader import render_to_string

channel_layer = get_channel_layer()
def createNotification(type,user,text,url,chat_id=0):

    Notification.objects.create(
        type=type,
        user=user,
        text=text,
        chat_id=chat_id,
        url=url)

    try:
        async_to_sync(channel_layer.send)(user.channel, {"type": "user.notify",
                                                         'event':type,
                                                         'message':text,
                                                         'url':url})
        msg_html = render_to_string('notification.html', {'message': text,
                                                          'event': type})
        send_mail('Новое оповещение Pandiga ', None, 'info@pandiga.ru', [user.email],
                  fail_silently=False, html_message=msg_html)
    except:
        print('user offline')
