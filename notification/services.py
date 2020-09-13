from .models import *

def createNotification(type,user,text,url):
    Notification.objects.create(
        type=type,
        user=user,
        text=text,
        url=url)