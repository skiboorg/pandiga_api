# Generated by Django 3.0.8 on 2020-09-17 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20200917_0825'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_activity',
        ),
        migrations.AlterField(
            model_name='user',
            name='last_online',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Последний раз был онлайн'),
        ),
    ]
