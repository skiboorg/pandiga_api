from django.db import models
from pytils.translit import slugify
from django.utils.safestring import mark_safe

from django.core.files import File
from user.models import User
from technique.services import *
from city.models import City


class TechniqueFilter(models.Model):
    """Фильтр еденицы техники"""
    name = models.CharField('Название фильтра', max_length=255, blank=False, null=True)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    type = models.CharField('Тип фильтра', max_length=255, blank=False, null=True)
    placeholder = models.CharField('Placeholder', max_length=255,blank=True, default='')
    from_placeholder = models.CharField('From placeholder', max_length=255,blank=True, default='')
    to_placeholder = models.CharField('To placeholder', max_length=255,blank=True, default='')
    from_value = models.CharField('from_value', max_length=255,blank=True, default='')
    to_value = models.CharField('to_value', max_length=255, blank=True,default='')
    value = models.CharField('value', max_length=255,blank=True, default='')
    title = models.CharField('Заголовок блока фильра', max_length=255,blank=True, default='')
    #Первичный фильтр расположен на еденице техники
    is_primary_filter = models.BooleanField('Первичный фильтр?', default=False)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = slugify(self.name)
        self.name_slug = slug
        super(TechniqueFilter, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Фильтр"
        verbose_name_plural = "Фильтры"

class TechniqueFilterValue(models.Model):
    """Значение фильтр еденицы техники"""
    filter = models.ForeignKey(TechniqueFilter, blank=True, null=True, db_index=True,
                               on_delete=models.SET_NULL,verbose_name='Фильтр',
                               related_name='values')
    label = models.CharField('label', max_length=255, blank=True, null=True)
    label_lower = models.CharField('label', max_length=255, blank=True, null=True, editable=False)
    value = models.CharField('value', max_length=255, blank=True, null=True)
    is_show_in_item_card = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.label_lower = self.label.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.filter.name} {self.label}'


    def __str__(self):
        return f'{self.label} - {self.label}'

    class Meta:
        verbose_name = "Значение фильтра"
        verbose_name_plural = "Значения фильтров"

class TechniqueCategory(models.Model):
    """Категория техники"""
    name = models.CharField('Категория техники', max_length=255, blank=False, null=True)
    image = models.ImageField('Изображение (265 x 185)', upload_to='technique/type/', blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    page_h1 = models.CharField('Тег H1 (если не указан, выводится название категории) ',
                                max_length=255, blank=True, null=True)
    page_title = models.CharField('Название страницы SEO', max_length=255, blank=True, null=True)
    page_description = models.CharField('Описание страницы SEO', max_length=255, blank=True, null=True)
    page_keywords = models.TextField('Keywords SEO', blank=True, null=True, editable=False)
    seo_text = models.TextField('СЕО текст на страницу. ', blank=True, null=True)
    views = models.IntegerField('Просмотров категории', blank=True, default=0)
    price = models.IntegerField('Стоимость размещения', blank=False, null=True)
    is_active = models.BooleanField('Отображается на сайте?', default=True)
    is_show_at_index = models.BooleanField('Отображается на главной?', default=False)

    def save(self, *args, **kwargs):
        self.name_lower = self.name.lower()
        if not self.name_slug:
            slug = slugify(self.name)
            testSlug = TechniqueCategory.objects.filter(name_slug=slug)
            if testSlug.exists():
                self.name_slug = f'{slug}-{create_slug(2)}'
            else:
                self.name_slug = slug
        super(TechniqueCategory, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name_slug}'

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class TechniqueType(models.Model):
    """Тип техники"""
    category = models.ForeignKey(TechniqueCategory, blank=True, null=True, db_index=True,
                                 on_delete=models.SET_NULL,
                                 related_name='types',
                                 verbose_name='Категория')
    filters = models.ManyToManyField(TechniqueFilter, blank=True,
                                     verbose_name='Фильтры',
                                     related_name='filters')
    name = models.CharField('Категория техники', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)

    def get_orders_count(self):

        from order.models import Order
        orders = Order.objects.filter(type_id=self.id,is_moderated=True, is_finished=False, is_active=True,worker__isnull=True)
        return orders.count()

    def save(self, *args, **kwargs):
        self.name_lower = self.name.lower()
        if not self.name_slug:
            slug = slugify(self.name)
            testSlug = TechniqueType.objects.filter(name_slug=slug)
            if testSlug.exists():
                self.name_slug = f'{slug}-{create_slug(2)}'
            else:
                self.name_slug = slug
        super(TechniqueType, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name_slug}'

    class Meta:
        verbose_name = "Тип техники"
        verbose_name_plural = "Типы техники"


class TechniqueUnit(models.Model):
    """Еденица техники"""
    type = models.ForeignKey(TechniqueType, blank=True, null=True, db_index=True, on_delete=models.SET_NULL,
                             verbose_name='Тип техники')
    owner = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                              verbose_name='Владелец', related_name='units')
    filter = models.ManyToManyField(TechniqueFilter, blank=True,
                                     verbose_name='Фильтры',
                                     related_name='unit_filters')
    filter_value = models.ManyToManyField(TechniqueFilterValue, blank=True,
                                     verbose_name='ФильтрыЗначения',
                                     related_name='unit_filter_values')
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL,
                             verbose_name='Местоположение')

    coords = models.CharField('Координаты', max_length=255, blank=True, null=True)
    name = models.CharField('Название техники', max_length=255, blank=False, null=True)
    name_lower = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    name_slug = models.CharField(max_length=255, blank=True, null=True, db_index=True, editable=False)
    min_rent_time = models.IntegerField('Минимальное время аренды', blank=False, null=True)
    #rent_type усли True почасовая, если False посуточная
    rent_type = models.BooleanField('Тип аренды почасовая', default=True)
    rent_price = models.IntegerField('Стоимость аренды', blank=False, null=True)
    description = models.TextField('Описание', blank=False, null=True)
    features = models.TextField('Характеристики', blank=False, null=True)
    year = models.IntegerField('Год', blank=True, null=True)
    rating = models.IntegerField('Рейтинг', default=0)
    rate_times = models.IntegerField('Кол-во отзывов', default=0)
    ad_price = models.IntegerField('Стоимость объявления', default=0)
    rate_value = models.IntegerField('Сумма оценок', default=0)
    is_moderated = models.BooleanField('Проверена?', default=True)
    is_vip = models.BooleanField('ВИП?', default=False)
    in_rent = models.BooleanField('В аренде?', default=False)
    is_free = models.BooleanField('Статус свободен?', default=True)
    is_active = models.BooleanField('Учавстует в выдаче?', default=True)
    views = models.IntegerField('Просмотров', default=0)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)
    promote_at = models.DateTimeField("Дата поднятия", auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name_lower = self.name.lower()
        if self.owner.is_vip:
            self.is_vip = True
        self.ad_price = self.city.coefficient * self.type.category.price
        if not self.name_slug:
            slug = slugify(self.name)
            testSlug = TechniqueUnit.objects.filter(name_slug=slug)
            if testSlug.exists():
                self.name_slug = f'{slug}-{create_slug(2)}'
            else:
                self.name_slug = slug
        super(TechniqueUnit, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('-is_vip','-promote_at')
        verbose_name = "Еденица техники"
        verbose_name_plural = "Еденицы техники"

    def get_filter_value(self):
        result=[]
        filters = self.filter.all()
        values = self.filter_value.all()

        for filter in filters:
            for value in values:
                if value.filter.name_slug == filter.name_slug:
                    result.append({
                            filter.name_slug:value.value
                        })
            # print('filter',filter.id)

        # print(result)
        return result




class TechniqueUnitFeedback(models.Model):
    techniqueitem = models.ForeignKey(TechniqueUnit, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name='Отзыв для', related_name='unit_feedbacks')
    author = models.ForeignKey(User, blank=False, null=True, on_delete=models.CASCADE,
                                      verbose_name='Отзыв от')
    text = models.TextField('Тест', blank=True, null=True)
    value = models.IntegerField('Оценка', blank=True, null=True)
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.text and self.value:
            set_unit_rating(self.techniqueitem.id,self.value)
        super(TechniqueUnitFeedback, self).save(*args, **kwargs)

class TechniqueUnitImage(models.Model):
    techniqueitem = models.ForeignKey(TechniqueUnit, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name='Изображение для',related_name='images')
    image = models.ImageField('Изображение', upload_to='technique/items/', blank=False, null=True)
    image_thumb = models.ImageField('Изображение уменьшенное', upload_to='technique/items/', blank=True, null=True,editable=False)
    is_moderated = models.BooleanField('Изображение проверено?', default=True)

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))

    image_tag.short_description = 'Изображение'

    def save(self, *args, **kwargs):
        self.image.save(f'{self.techniqueitem.name_slug}.jpg',File(image_resize_and_watermark(self.image,True,0,0)), save=False)
        self.image_thumb.save(f'{self.techniqueitem.name_slug}-thumb.jpg',File(image_resize_and_watermark(self.image,False,240,180)), save=False)
        super(TechniqueUnitImage, self).save(*args, **kwargs)

class TechniqueUnitImageDoc(models.Model):
    techniqueitem = models.ForeignKey(TechniqueUnit, blank=False, null=True, on_delete=models.CASCADE,
                                verbose_name='Документы для',related_name='docs')
    image = models.ImageField('Документы', upload_to='technique/items/', blank=False, null=True)

    def image_tag(self):
        return mark_safe('<img src="{}" width="100" height="100" />'.format(self.image.url))

    image_tag.short_description = 'Документы'



