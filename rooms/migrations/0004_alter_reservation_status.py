# Generated by Django 3.2.13 on 2022-07-14 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0003_roomsapplicationmodel_views'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.BooleanField(default=True, verbose_name='Бронь подтверждена?'),
        ),
    ]