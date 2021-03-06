# Generated by Django 3.0.8 on 2020-09-21 14:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_paymentobj_pay_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='refferals',
        ),
        migrations.CreateModel(
            name='Refferals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('master', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='master_user', to=settings.AUTH_USER_MODEL)),
                ('slaves', models.ManyToManyField(null=True, related_name='slaves', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
