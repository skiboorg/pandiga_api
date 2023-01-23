from .models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.mail import send_mail
from django.template.loader import render_to_string
import settings
from pyfcm import FCMNotification

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
                                                         'url':url,
                                                         'chat_id':chat_id})
        msg_html = render_to_string('notify.html', {'message': text,
                                                          'event': type})
        send_mail('Новое оповещение Pandiga ', None, 'info@pandiga.ru', [user.email],
                  fail_silently=False, html_message=msg_html)

    except:
        print('user offline')

    if user.notification_id:

        push_service = FCMNotification(api_key=settings.FCM_API_KEY)

        registration_id = user.notification_id
        message_title = 'Оповещение'
        message_body = text

        if type == 'chat':
            data_message = {
                "url": f'/profile/chat/{chat_id}'
            }
        else:
            data_message = {
                "url": url
            }

        result = push_service.notify_single_device(registration_id=registration_id,
                                                   sound='Default',
                                                   message_title=message_title,
                                                   message_body=message_body,
                                                   data_message=data_message,
                                                   )
        print(result)
