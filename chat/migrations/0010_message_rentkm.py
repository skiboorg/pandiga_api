# Generated by Django 4.0.6 on 2022-11-23 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0009_auto_20210323_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='rentKm',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]