# Generated by Django 4.0.6 on 2022-11-22 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0028_alter_techniqueunit_promote_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='techniqueunit',
            name='rent_type',
            field=models.BooleanField(blank=True, null=True, verbose_name='Тип аренды почасовая'),
        ),
    ]
