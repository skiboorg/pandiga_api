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
    favorites = models.ManyToManyField('technique.TechniqueUnit', blank=True, verbose_name='Избранное')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL,
                             verbose_name='Местоположение')
    avatar = models.ImageField('Фото', upload_to='user',default='profile.svg')
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
    used_partner_code = models.CharField('Партнерский код', max_length=100, blank=True, null=True, unique=True)
    balance = models.IntegerField('Баланс', default=0)
    orders_count = models.IntegerField('Размещено заказов', default=0)
    rent_count = models.IntegerField('Взято в аренду', default=0)
    partner_balance = models.IntegerField('Партнерский баланс', default=1000)
    rating = models.IntegerField('Рейтинг', default=0)
    rate_times = models.IntegerField('Кол-во отзывов', default=0)
    rate_value = models.IntegerField('Сумма оценок', default=0)
    vip_update = models.DateField('Дата начала тарифа', blank=True, null=True)
    vip_expire = models.DateField('Дата завершения тарифа', blank=True, null=True)
    last_online = models.DateTimeField('Последний раз был онлайн', auto_now=True, null=True)
    is_vip = models.BooleanField('VIP?', default=False)
    is_ref_code_entered = models.BooleanField('Код введен', default=False)
    is_online = models.BooleanField('Онлайн?', default=False)
    is_customer = models.BooleanField('Заказчик?', default=True)
    is_person = models.BooleanField('Частное лицо?', default=True)
    is_verified = models.BooleanField('Акканнт подтвержден?', default=False)
    is_phone_verified = models.BooleanField('Телефон подтвержден?', default=False)
    is_email_verified = models.BooleanField('EMail подтвержден?', default=False)
    verify_code = models.CharField('Код подтверждения', max_length=50, blank=True, null=True)
    notification_id = models.CharField('ID для сообщений', max_length=255, blank=True, null=True, unique=True)
    channel = models.CharField(max_length=255,blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.get_full_name()} {self.phone}'

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
        if self.is_person:
            if self.first_name and self.last_name:
                return f'{self.first_name} {self.last_name}'
            elif self.first_name and not self.last_name:
                return f'{self.first_name}'
            elif not self.first_name and not self.last_name:
                return 'Неизвестный пользователь'
        else:
            return f'{self.organization_name}'


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

    class Meta:
        ordering = ('-created_at',)



def user_feedback_post_save(sender, instance, created, **kwargs):
    if created:
        instance.user.rate_times += 1
        instance.user.rate_value += instance.value
        instance.user.rating = round(instance.user.rate_value / instance.user.rate_times)
        instance.user.save(update_fields=['rate_times', 'rate_value', 'rating'])

post_save.connect(user_feedback_post_save, sender=UserFeedback)

class PaymentType(models.Model):
    icon = models.ImageField('Иконка', upload_to='payment/', blank=False, null=True)
    name = models.CharField('Название платежа', max_length=255, blank=True, null=True)
    method = models.CharField('Метод платежа', max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Отображать?', default=True)

    def __str__(self):
        return self.name or ''

    class Meta:
        verbose_name = "Вид платежа"
        verbose_name_plural = "Виды платежей"

class PaymentObj(models.Model):
    pay_id = models.CharField('ID платежа',max_length=255,blank=True,null=True)
    pay_code = models.CharField('ID платежа',max_length=255,blank=True,null=True)
    user = models.ForeignKey(User, blank=False, null=True,
                                  on_delete=models.CASCADE,
                                  verbose_name='Пользователь')
    type = models.ForeignKey(PaymentType, blank=False, null=True,
                                  on_delete=models.CASCADE,
                                  verbose_name='Вид платежа')
    status = models.CharField('Статус платежа', max_length=255,blank=True,null=True)
    amount = models.IntegerField('Сумма платежа', blank=True,null=True)
    is_payed = models.BooleanField("Оплачен?", default=False)
    created_at = models.DateTimeField("Дата платежа", auto_now_add=True)

    def __str__(self):
        return f'Платеж от {self.created_at}. На сумму {self.amount}. Статус {self.status}'

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"



class Settings(models.Model):
    is_free = models.BooleanField("Размещение платное", default=False)
    vip_price = models.IntegerField('Надбавки за ВИП услуги', default=0)
    up_price = models.IntegerField('Цена поднятия, если не указано, будет использована цена объявления', default=0)
    vip_time = models.IntegerField('Интервал ВИП услуг (поднять и закрепить) ХХ дней', default=30)

    def __str__(self):
        return f'Настройки'

class Refferal(models.Model):
    """Начисления партеров"""
    master = models.ForeignKey(User, blank=True, null=True,
                               on_delete=models.CASCADE,
                               related_name='master_user_money')
    refferal = models.ForeignKey(User,blank=True,null=True,
                             on_delete=models.CASCADE,
                             verbose_name='Рефферал')
    earned = models.IntegerField('Начислено', default=0)
    action = models.CharField('Операция', max_length=10, blank=True,null=True, default=0)
    created_at = models.DateTimeField("Дата начисления", auto_now_add=True)

    def __str__(self):
        return f'Начисление от  {self.refferal.id}'

    class Meta:
        verbose_name = "Начисление"
        verbose_name_plural = "Начисления"

def user_post_save(sender, instance, created, **kwargs):
    """Создание всех значений по-умолчанию для нового пользовыателя"""
    if created:
        instance.partner_code = create_random_string(digits=True,num=8)
        instance.save()

post_save.connect(user_post_save, sender=User)