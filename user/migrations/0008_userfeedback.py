# Generated by Django 3.0.8 on 2020-09-13 10:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20200906_1048'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Тест')),
                ('value', models.IntegerField(blank=True, null=True, verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_feedback', to=settings.AUTH_USER_MODEL, verbose_name='Отзыв от')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='for_feedback', to=settings.AUTH_USER_MODEL, verbose_name='Отзыв для')),
            ],
        ),
    ]
