# Generated by Django 4.0.6 on 2022-11-22 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('city', '0002_alter_city_options_city_order_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ('order_num', 'city'), 'verbose_name': 'Город', 'verbose_name_plural': 'Города и регионы'},
        ),
    ]
