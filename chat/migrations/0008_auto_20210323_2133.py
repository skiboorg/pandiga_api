# Generated by Django 3.1.5 on 2021-03-23 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0024_auto_20210320_1207'),
        ('chat', '0007_auto_20200923_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='rentEndDate',
            new_name='rentDays',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='rentEndTime',
            new_name='rentHours',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='rentStartTime',
            new_name='rentTime',
        ),
        migrations.RemoveField(
            model_name='message',
            name='rentStartDate',
        ),
        migrations.AlterField(
            model_name='message',
            name='rentUnit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='technique.techniqueunit', verbose_name='Техника для аренды в сообщении'),
        ),
    ]
