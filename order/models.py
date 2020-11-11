from django.db import models
from technique.models import *
from user.models import User
from city.models import City
from technique.services import create_slug

class Order(models.Model):
    type = models.ForeignKey(TechniqueType, blank=True, null=True, on_delete=models.SET_NULL,
                             verbose_name='Относится к типу')

    owner = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL,
                              verbose_name='Заказчик', related_name='owner')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL,
                              verbose_name='Местоположение')
    worker = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                              verbose_name='Исполнитель', related_name='worker')
    worker_unit = models.ForeignKey(TechniqueUnit, blank=True, null=True, on_delete=models.SET_NULL,
                              verbose_name='Исполнитель', related_name='worker_unit')
    filter = models.ManyToManyField(TechniqueFilter, blank=True,
                                    verbose_name='Фильтры',
                                    related_name='order_filters')
    filter_value = models.ManyToManyField(TechniqueFilterValue, blank=True,
                                          verbose_name='ФильтрыЗначения',
                                          related_name='order_filter_values')
    coords = models.CharField('Координаты', max_length=255, blank=True, null=True)
    apply_units = models.ManyToManyField(TechniqueUnit, verbose_name='Предложенная техника',related_name='apply_units')
    decline_units = models.ManyToManyField(TechniqueUnit, verbose_name='Отказы техники',related_name='decline_units')
    name = models.CharField('Название', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    rent_time = models.IntegerField('Время аренды', blank=False, null=True)
    # rent_type усли True почасовая, если False посуточная
    rent_type = models.BooleanField('Тип аренды почасовая', default=True)
    rentDate = models.DateField(blank=True, null=True)
    rentStartDate = models.DateField(blank=True, null=True)
    rentEndDate = models.DateField(blank=True, null=True)
    rentStartTime = models.TimeField(blank=True, null=True)
    rentEndTime = models.TimeField(blank=True, null=True)
    comment = models.TextField('Описание', blank=False, null=True)
    is_moderated = models.BooleanField('Проверена?', default=True)
    is_active = models.BooleanField('Учавстует в выдаче?', default=True)
    is_finished = models.BooleanField('Выполнена?', default=False)
    views = models.IntegerField('Просмотров',default=0)
    customer_feedback = models.BooleanField('Отзыв от заказчика', default=False)
    worker_feedback = models.BooleanField('Отзыв от исполнителя', default=False)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    update_at = models.DateTimeField("Дата изменения", auto_now=True)

    def save(self, *args, **kwargs):
        self.name_lower = self.name.lower()
        self.owner.orders_count += 1
        self.owner.save()
        if not self.name_slug:
            slug = slugify(self.name)
            testSlug = Order.objects.filter(name_slug=slug)
            if testSlug.exists():
                self.name_slug = f'{slug}-{create_slug(2)}'
            else:
                self.name_slug = slug

        super(Order, self).save(*args, **kwargs)

