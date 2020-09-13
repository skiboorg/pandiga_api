from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save

from city.models import City
from .services import *


class UserManager(BaseUserManager):
    use_in_migrations = True
    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    # tarif = models.ForeignKey(Tarif,blank=True,null=True,on_delete=models.SET_NULL,
    #                           related_name='Тариф')
    # own_partner_code = models.ForeignKey(ParnterCode,blank=True,null=True,
    #                                      on_delete=models.SET_NULL,
    #                                      related_name='own_partner_code',
    #                                      verbose_name='Персональный портнерский код')
    subscribe_type = models.ManyToManyField('technique.TechniqueType', blank=True, verbose_name='Тип техники для оповещений')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL,
                             verbose_name='Местоположение')
    avatar = models.ImageField('Фото', upload_to='user',blank=True,null=True)
    photo = models.CharField('VK аватар', max_length=255, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=50, blank=True, null=True, default='Иван')
    last_name = models.CharField('Фамилия', max_length=50, blank=True, null=True, default='Иванов')
    organization_name = models.CharField('Название организации', max_length=50, blank=True, null=True)
    inn = models.CharField('ИНН', max_length=50, blank=True, null=True)
    ogrn = models.CharField('ОГРН', max_length=50, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=50, blank=True, null=True, unique=True)
    email = models.EmailField('Эл. почта', blank=True, null=True, unique=True)
    birthday = models.DateField('День рождения', blank=True, null=True)
    partner_code = models.CharField('Партнерский код', max_length=100, blank=True, null=True, unique=True)
    balance = models.IntegerField('Баланс', default=0)
    orders_count = models.IntegerField('Размещено заказов', default=0)
    rent_count = models.IntegerField('Взято в аренду', default=0)
    partner_balance = models.IntegerField('Партнерский баланс', default=0)
    rating = models.IntegerField('Рейтинг', default=0)
    rate_times = models.IntegerField('Кол-во отзывов', default=0)
    rate_value = models.IntegerField('Сумма оценок', default=0)
    vip_update = models.DateField('Дата начала тарифа', blank=True, null=True)
    vip_expire = models.DateField('Дата завершения тарифа', blank=True, null=True)
    is_vip = models.BooleanField('VIP?', default=False)
    is_customer = models.BooleanField('Заказчик?', default=True)
    is_person = models.BooleanField('Частное лицо?', default=True)
    is_verified = models.BooleanField('Акканнт подтвержден?', default=False)
    is_phone_verified = models.BooleanField('Телефон подтвержден?', default=False)
    is_email_verified = models.BooleanField('EMail подтвержден?', default=False)
    verify_code = models.CharField('Код подтверждения', max_length=50, blank=True, null=True)
    notification_id = models.CharField('ID для сообщений', max_length=100, blank=True, null=True, unique=True)

    last_activity = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    # def __str__(self):
    #     if self.phone:
    #         return f'{self.get_full_name()} {self.phone}'
    #     elif self.email:
    #         return f'{self.get_full_name()} {self.email}'
    #     else:
    #         return f'{self.get_full_name()} {self.id}'
    #
    # def get_user_activity(self):
    #     if (timezone.now() - self.last_activity) > dt.timedelta(seconds=10):
    #         return f'Был {self.last_activity.strftime("%d.%m.%Y,%H:%M:%S")}'
    #     else:
    #         return 'В сети'
    #
    #
    # def get_rating(self):
    #     try:
    #         return round(self.rating / self.rate_times)
    #     except:
    #         return 0

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name and not self.last_name:
            return f'{self.first_name}'
        elif not self.first_name and not self.last_name:
            return 'Неизвестный пользователь'


    # def get_avatar(self):
    #     if self.avatar:
    #         return self.avatar.url
    #     else:
    #         return '/static/img/no_ava.jpg'

class UserFeedback(models.Model):
    user = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name='Отзыв для', related_name='for_feedback')
    author = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name='Отзыв от', related_name='from_feedback')
    text = models.TextField('Тест', blank=True, null=True)
    value = models.IntegerField('Оценка', blank=True, null=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.text and self.value:
            set_user_rating(self.user.id,self.value)
        super(UserFeedback, self).save(*args, **kwargs)


def user_post_save(sender, instance, created, **kwargs):
    """Создание всех значений по-умолчанию для нового пользовыателя"""
    if created:
        instance.partner_code = create_random_string(digits=True,num=8)
        instance.save()

post_save.connect(user_post_save, sender=User)