from django.db import models

class City(models.Model):
    city = models.CharField('Город',
                            max_length=50,
                            blank=True,
                            null=True,
                            db_index=True)
    cityAlias = models.CharField('Склонение города (должно отвечать на вопрос ГДЕ, например, Москве)',
                                 max_length=30,
                                 blank=False,
                                 null=True)
    region = models.CharField('Регион',
                              max_length=100,
                              blank=True,
                              null=True,
                              db_index=True)
    coefficient = models.DecimalField('Коэффициент стоимости размещения',
                                      decimal_places=2,
                                      max_digits=3,
                                      default=1)
    sub_domain = models.CharField('Название поддомена(на пример msk)',
                                  max_length=50,
                                  blank=True,
                                  null=True,
                                  db_index=True)
    is_default = models.BooleanField('Домен по умолчанию?',default=False)

    def __str__(self):
        return f'{self.city}'

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города и регионы"
