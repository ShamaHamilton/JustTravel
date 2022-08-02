# Generated by Django 3.2.13 on 2022-08-02 19:59

import blogs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_rename_interestingplaces_places'),
    ]

    operations = [
        migrations.AddField(
            model_name='localities',
            name='preview',
            field=models.ImageField(blank=True, upload_to=blogs.models.localities_preview_upload_to, verbose_name='превью'),
        ),
        migrations.AddField(
            model_name='places',
            name='preview',
            field=models.ImageField(blank=True, upload_to=blogs.models.places_preview_upload_to, verbose_name='изображение'),
        ),
    ]