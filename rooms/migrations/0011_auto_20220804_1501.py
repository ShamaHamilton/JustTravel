# Generated by Django 3.2.13 on 2022-08-04 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0010_auto_20220803_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomsapplicationmodel',
            name='session_hash',
        ),
        migrations.RemoveField(
            model_name='roomsapplicationmodel',
            name='stage',
        ),
        migrations.AddField(
            model_name='roomsapplicationmodel',
            name='map_location',
            field=models.TextField(blank=True, verbose_name='расположение на карте'),
        ),
    ]