# Generated by Django 3.0.8 on 2020-08-10 09:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('technique', '0012_auto_20200810_0855'),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='isRentMessage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='rentUnit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='technique.TechniqueUnit', verbose_name='В чате'),
        ),
        migrations.AlterField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.Chat', verbose_name='В чате'),
        ),
    ]
