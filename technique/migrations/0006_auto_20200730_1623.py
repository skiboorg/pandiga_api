# Generated by Django 3.0.8 on 2020-07-30 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0005_auto_20200730_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techniquefilter',
            name='from_placeholder',
            field=models.CharField(default='', max_length=255, verbose_name='From placeholder'),
        ),
        migrations.AlterField(
            model_name='techniquefilter',
            name='from_value',
            field=models.CharField(default='', max_length=255, verbose_name='from_value'),
        ),
        migrations.AlterField(
            model_name='techniquefilter',
            name='placeholder',
            field=models.CharField(default='', max_length=255, verbose_name='Placeholder'),
        ),
        migrations.AlterField(
            model_name='techniquefilter',
            name='title',
            field=models.CharField(default='', max_length=255, verbose_name='Заголовок блока фильра'),
        ),
        migrations.AlterField(
            model_name='techniquefilter',
            name='to_placeholder',
            field=models.CharField(default='', max_length=255, verbose_name='To placeholder'),
        ),
        migrations.AlterField(
            model_name='techniquefilter',
            name='to_value',
            field=models.CharField(default='', max_length=255, verbose_name='to_value'),
        ),
    ]
