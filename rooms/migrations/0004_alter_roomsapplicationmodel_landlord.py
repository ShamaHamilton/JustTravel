# Generated by Django 3.2.13 on 2022-06-30 19:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0003_roomsapplicationmodel_landlord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomsapplicationmodel',
            name='landlord',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='landlord', to=settings.AUTH_USER_MODEL, verbose_name='хозяин жилья'),
        ),
    ]
