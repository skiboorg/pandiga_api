import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from celery import shared_task
from .models import *
import settings
from notification.models import Notification
from user.models import Settings
def send_email(title,to,data):
    msg_html = render_to_string('notify.html', data)
    send_mail(title, None, settings.SMTP_FROM, [to],
              fail_silently=False, html_message=msg_html)

@shared_task
def check_technique():
    all_vip = TechniqueUnit.objects.filter(is_vip=True)

    for vip in all_vip:
        site_settings = Settings.objects.get(id=1)
        print(vip.promote_at.date() + datetime.timedelta(days=site_settings.vip_time-1))
        if datetime.date.today() == vip.promote_at.date() + datetime.timedelta(days=site_settings.vip_time-1) :
            Notification.objects.create(type='order',
                                        user=vip.owner,
                                        url='/profile',
                                        text=f'Услуга закрепления техники ({vip.name}) в поиске будет отключена через 24 часа.')
        if datetime.date.today() == vip.promote_at.date() + datetime.timedelta(days=site_settings.vip_time) :
            vip.is_vip = False
            vip.save()
            Notification.objects.create(type='order',
                                        user=vip.owner,
                                        url='/profile',
                                        text=f'Услуга закрепления техники ({vip.name}) в поиске отключена. Повторно активировать услуги можете Вы можете в своем личном кабинете.')
            # send_email('Услуга закрепления техники отключена',vip.owner.email,
            #            {"text":"Услуга закрепления техники в поиске отключена. Повторно активировать услуги можете Вы можете всвем личном кабинете."})