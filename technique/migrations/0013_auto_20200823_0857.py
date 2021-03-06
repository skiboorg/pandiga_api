# Generated by Django 3.0.8 on 2020-08-23 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('city', '0001_initial'),
        ('technique', '0012_auto_20200810_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='techniqueunit',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='city.City', verbose_name='Местоположение'),
        ),
        migrations.AlterField(
            model_name='techniqueunit',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='units', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
    ]
