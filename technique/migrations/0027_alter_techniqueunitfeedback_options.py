# Generated by Django 4.0.6 on 2022-10-09 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0026_auto_20210324_1050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='techniqueunitfeedback',
            options={'ordering': ('-created_at',)},
        ),
    ]
