import json
from technique.models import TechniqueUnit
from django.db import models
from user.models import User

class Chat(models.Model):

    users = models.ManyToManyField(User, blank=True,  verbose_name='Пользователи',
                                    related_name='chatusers')

    # techniqueitem = models.ForeignKey(TechniqueItem, blank=True, null=True, on_delete=models.CASCADE,
    #                                   verbose_name='Тема чата техника')
    # order = models.ForeignKey(TechniqueOrder, blank=True, null=True, on_delete=models.CASCADE,
    #                                   verbose_name='Тема чата заявка')
    isNewMessages = models.BooleanField('Есть новые сообщения', default=False)
    # lastMessageOwn = models.BooleanField( default=False)
    # lastMsgBy = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Сообщение от')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def get_last_message_text(self):
        try:
            return self.messages.last().message
        except:
            return ''

    def get_last_message_user_avatar(self):
        try:
            return self.messages.last().user.avatar.url
        except:
            return ''

    def get_last_message_user_id(self):
        try:
            return self.messages.last().user.id
        except:
            return ''

    def get_last_message_user_name(self):
        try:
            return self.messages.last().user.get_full_name()
        except:
            return ''


class Message(models.Model):
    chat = models.ForeignKey(Chat, blank=False, null=True, on_delete=models.CASCADE, verbose_name='В чате',
                             related_name='messages')
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE, verbose_name='Сообщение от')
    message = models.TextField('Сообщение', blank=True,null=True)
    isUnread = models.BooleanField('Не прочитанное сообщение', default=True)
    isRentMessage = models.BooleanField( default=False)
    rentUnit = models.ForeignKey(TechniqueUnit, blank=True, null=True,
                                  on_delete=models.CASCADE, verbose_name='В чате')
    # rentType усли True почасовая, если False посуточная
    rentType = models.BooleanField(default=True)
    rentDate = models.DateField(blank=True,null=True)
    rentStartDate = models.DateField(blank=True,null=True)
    rentEndDate = models.DateField(blank=True,null=True)
    rentStartTime = models.TimeField(blank=True,null=True)
    rentEndTime = models.TimeField(blank=True,null=True)

    createdAt = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.isUnread:
            self.chat.isNewMessages = True
            self.chat.save()

        super(Message, self).save(*args, **kwargs)
