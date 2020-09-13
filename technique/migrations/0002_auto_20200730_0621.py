# Generated by Django 3.0.8 on 2020-07-30 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('technique', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='techniqueunit',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='techniques', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='techniqueunit',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='technique.TechniqueType', verbose_name='Тип техники'),
        ),
        migrations.AddField(
            model_name='techniquetype',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='technique.TechniqueCategory', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='techniquetype',
            name='filters',
            field=models.ManyToManyField(blank=True, related_name='filters', to='technique.TechniqueFilter', verbose_name='Фильтры'),
        ),
        migrations.AddField(
            model_name='techniquefiltervalue',
            name='filter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='filter', to='technique.TechniqueFilter', verbose_name='Фильтр'),
        ),
    ]
