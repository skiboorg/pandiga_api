# Generated by Django 3.0.8 on 2020-09-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0016_auto_20200823_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='techniquetype',
            name='orders_count',
            field=models.IntegerField(default=0),
        ),
    ]
