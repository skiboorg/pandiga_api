# Generated by Django 3.0.8 on 2020-08-23 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0015_techniqueunit_coords'),
    ]

    operations = [
        migrations.AddField(
            model_name='techniqueunit',
            name='promote_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата поднятия'),
        ),
        migrations.AlterField(
            model_name='techniqueunit',
            name='is_vip',
            field=models.BooleanField(default=False, verbose_name='ВИП?'),
        ),
    ]
