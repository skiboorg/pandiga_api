from django.db import models
from user.models import User


class Notification(models.Model):
    type = models.CharField(max_length=255,blank=True,null=True)
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL,
                              verbose_name='Юзер')
    is_new = models.BooleanField(default=True)
    text = models.CharField(max_length=255,blank=True,null=True)
    url = models.CharField(max_length=255,blank=True,null=True)
    is_user_notified = models.BooleanField(default=False)
    is_delayed = models.BooleanField(default=False)
    show_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True, null=True)