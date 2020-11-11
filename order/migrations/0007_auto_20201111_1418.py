# Generated by Django 3.0.8 on 2020-11-11 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0022_techniquefiltervalue_label_lower'),
        ('order', '0006_order_coords'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='decline_units',
            field=models.ManyToManyField(related_name='decline_units', to='technique.TechniqueUnit', verbose_name='Отказы техники'),
        ),
        migrations.AlterField(
            model_name='order',
            name='apply_units',
            field=models.ManyToManyField(related_name='apply_units', to='technique.TechniqueUnit', verbose_name='Предложенная техника'),
        ),
    ]
