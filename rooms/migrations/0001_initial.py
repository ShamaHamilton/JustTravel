# Generated by Django 3.2.13 on 2022-06-30 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomsApplicationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_hash', models.CharField(max_length=40, unique=True)),
                ('stage', models.CharField(default='1', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('owner', models.CharField(blank=True, max_length=255, verbose_name='владелец')),
                ('status', models.BooleanField(default=False, verbose_name='объявление опубликовано?')),
                ('housing', models.CharField(blank=True, max_length=100, verbose_name='какое у вас жилье?')),
                ('housing_type', models.CharField(blank=True, max_length=100, verbose_name='что из перечисленного точнее описывает ваше жилье?')),
                ('offer_type', models.CharField(blank=True, max_length=100, verbose_name='что вы предлагаете?')),
                ('location', models.CharField(blank=True, max_length=255, verbose_name='где расположено ваше жилье?')),
                ('number_of_guests', models.CharField(blank=True, max_length=10, verbose_name='сколько гостей вы готовы принять?')),
                ('special_amenities', models.CharField(blank=True, max_length=255, verbose_name='есть ли у вас особые удобства?')),
                ('popular_amenities', models.CharField(blank=True, max_length=255, verbose_name='вы предлагаете эти популярные среди гостей удобства?')),
                ('safety', models.CharField(blank=True, max_length=255, verbose_name='у вас есть указанные средства безопасности?')),
                ('photos', models.CharField(blank=True, max_length=255, verbose_name='добавьте несколько фото жилья')),
                ('housing_header', models.CharField(blank=True, max_length=50, verbose_name='придумайте яркое название жилья')),
                ('housing_description', models.TextField(blank=True, max_length=500, verbose_name='описание жилья')),
                ('price', models.CharField(blank=True, max_length=255, verbose_name='установите цену')),
            ],
            options={
                'verbose_name': 'жилье',
                'verbose_name_plural': 'жилье',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='прибытие')),
                ('end_date', models.DateField(verbose_name='выезд')),
                ('days_total', models.IntegerField(blank=True, null=True, verbose_name='всего дней')),
                ('price_total', models.IntegerField(blank=True, null=True, verbose_name='итоговая цена')),
                ('status', models.BooleanField(default=False, verbose_name='Бронь подтверждена?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата бронирования')),
                ('name_reserv', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='name_reserv', to=settings.AUTH_USER_MODEL, verbose_name='имя пользователя')),
            ],
            options={
                'verbose_name': 'резерв жилья',
                'verbose_name_plural': 'резерв жилья',
                'ordering': ['created_at'],
            },
        ),
    ]
