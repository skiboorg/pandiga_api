# Generated by Django 3.0.8 on 2020-08-10 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200806_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=True, verbose_name='Заказчик?'),
        ),
    ]
