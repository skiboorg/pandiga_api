# Generated by Django 3.0.8 on 2020-07-30 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TechniqueCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Категория техники')),
                ('image', models.ImageField(null=True, upload_to='technique/type/', verbose_name='Изображение (370 x 130)')),
                ('name_lower', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('page_h1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Тег H1 (если не указан, выводится название категории) ')),
                ('page_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название страницы SEO')),
                ('page_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание страницы SEO')),
                ('page_keywords', models.TextField(blank=True, editable=False, null=True, verbose_name='Keywords SEO')),
                ('seo_text', models.TextField(blank=True, null=True, verbose_name='СЕО текст на страницу. ')),
                ('views', models.IntegerField(blank=True, default=0, verbose_name='Просмотров категории')),
                ('is_active', models.BooleanField(default=True, verbose_name='Отображается на сайте?')),
            ],
        ),
        migrations.CreateModel(
            name='TechniqueFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название фильтра')),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('type', models.CharField(max_length=255, null=True, verbose_name='Тип фильтра')),
                ('placeholder', models.CharField(blank=True, max_length=255, null=True, verbose_name='Placeholder')),
                ('from_placeholder', models.CharField(blank=True, max_length=255, null=True, verbose_name='From placeholder')),
                ('to_placeholder', models.CharField(blank=True, max_length=255, null=True, verbose_name='To placeholder')),
                ('title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Заголовок блока фильра')),
                ('is_primary_filter', models.BooleanField(default=False, verbose_name='Первичный фильтр?')),
            ],
        ),
        migrations.CreateModel(
            name='TechniqueFilterValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='label')),
                ('value', models.CharField(blank=True, max_length=255, null=True, verbose_name='value')),
            ],
        ),
        migrations.CreateModel(
            name='TechniqueType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Категория техники')),
                ('name_lower', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TechniqueUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Название техники')),
                ('name_lower', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('name_slug', models.CharField(blank=True, db_index=True, editable=False, max_length=255, null=True)),
                ('min_rent_time', models.IntegerField(null=True, verbose_name='Минимальное время аренды')),
                ('rent_type_hour', models.BooleanField(default=True, verbose_name='Тип аренды почасовая')),
                ('rent_type_day', models.BooleanField(default=False, verbose_name='Тип аренды посуточная')),
                ('rent_price', models.IntegerField(null=True, verbose_name='Стоимость аренды')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('features', models.TextField(null=True, verbose_name='Характеристики')),
                ('rating', models.IntegerField(default=0, verbose_name='Рейтинг')),
                ('rate_times', models.IntegerField(default=0, verbose_name='РейтингT')),
                ('is_moderated', models.BooleanField(default=True, verbose_name='Проверена?')),
                ('is_vip', models.BooleanField(default=True, verbose_name='ВИП?')),
                ('is_free', models.BooleanField(default=True, verbose_name='Статус свободен?')),
                ('is_active', models.BooleanField(default=True, verbose_name='Учавстует в выдаче?')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотров')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('filter', models.ManyToManyField(blank=True, related_name='unit_filters', to='technique.TechniqueFilter', verbose_name='Фильтры')),
                ('filter_value', models.ManyToManyField(blank=True, related_name='unit_filters', to='technique.TechniqueFilterValue', verbose_name='ФильтрыЗначения')),
            ],
        ),
    ]
