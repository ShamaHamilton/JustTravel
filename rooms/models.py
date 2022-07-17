from distutils.command.upload import upload
from . import constants
from django.urls import reverse
from django.db import models
import hashlib
import random
import sys

from django.contrib.auth import get_user_model
User = get_user_model()


# from accounts.models import CustomCreateUser


def rooms_photo_upload_to(instance, filename):
    return f'rooms/{instance.landlord}/{instance.id}/{filename}'


def create_session_room_hash():
    hash = hashlib.sha1()
    hash.update(str(random.randint(0, sys.maxsize)).encode('utf-8'))
    return hash.hexdigest()


class RoomsApplicationModel(models.Model):
    session_hash = models.CharField(max_length=40, unique=True,)
    stage = models.CharField(max_length=10, default=constants.STAGE_1,)
    created_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='дата редактирования',
        auto_now=True,
    )
    status = models.BooleanField(
        verbose_name='объявление опубликовано?',
        default=False,
    )
    landlord = models.ForeignKey(       # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        User,
        on_delete=models.CASCADE,
        related_name='landlord',
        verbose_name='хозяин жилья',
        blank=True,
    )
    views = models.IntegerField(
        verbose_name='количество просмотров',
        default=0,
        blank=True,
    )
    # шаг 1: Какое у вас жилье?
    housing = models.CharField(
        verbose_name='какое у вас жилье?',
        max_length=100,
        blank=True,
    )
    # шаг 2: Что из перечисленного точнее описывает ваше жилье?
    housing_type = models.CharField(
        verbose_name='что из перечисленного точнее описывает ваше жилье?',
        max_length=100,
        blank=True,
    )
    # шаг 3: Что вы предлагаете?
    offer_type = models.CharField(
        verbose_name='что вы предлагаете?',
        max_length=100,
        blank=True,
    )
    # шаг 4: Где расположено ваше жилье? (на карте)
    location = models.CharField(
        verbose_name='где расположено ваше жилье?',
        max_length=255,
        blank=True,
    )
    # шаг 5: Сколько гостей вы готовы принять?
    guests = models.IntegerField(
        verbose_name='сколько гостей вы готовы принять?',
        blank=True,
    )
    beds = models.IntegerField(
        verbose_name='сколько у вас кроватей?',
        blank=True,
    )
    BATHROOM_CHOICES = (
        ('отдельная ванная', 'отдельная ванная'),
        ('отдельная душевая', 'отдельная душевая'),
        ('общая ванная', 'общая ванная'),
        ('общая душевая', 'общая душевая'),
        ('отсутствует', 'отсутствует'),
    )
    bathroom = models.CharField(
        verbose_name='какая у вас ванная комната?',
        max_length=17,
        choices=BATHROOM_CHOICES,
        blank=True,
    )
    # шаг 6: Удобства/Преимущества
    special_amenities = models.CharField(
        verbose_name='есть ли у вас особые удобства?',
        max_length=255,
        blank=True,
    )
    popular_amenities = models.CharField(
        verbose_name='вы предлагаете эти популярные среди гостей удобства?',
        max_length=255,
        blank=True,
    )
    safety = models.CharField(
        verbose_name='у вас есть указанные средства безопасности?',
        max_length=255,
        blank=True,
    )
    # шаг 7: Добавьте несколько фото жилья
    photo1 = models.ImageField(
        verbose_name='Фото 1',
        upload_to=rooms_photo_upload_to,
        max_length=255,
        blank=True,
    )
    photo2 = models.ImageField(
        verbose_name='Фото 2',
        upload_to=rooms_photo_upload_to,
        max_length=255,
        blank=True,
    )
    photo3 = models.ImageField(
        verbose_name='Фото 3',
        upload_to=rooms_photo_upload_to,
        max_length=255,
        blank=True,
    )
    photo4 = models.ImageField(
        verbose_name='Фото 4',
        upload_to=rooms_photo_upload_to,
        max_length=255,
        blank=True,
    )
    photo5 = models.ImageField(
        verbose_name='Фото 5',
        upload_to=rooms_photo_upload_to,
        max_length=255,
        blank=True,
    )
    # шаг 8: Придумайте яркий заголовок (название) жилья
    header = models.CharField(
        verbose_name='придумайте яркое название жилья',
        max_length=50,
        blank=True,
    )
    # шаг 9: Опишите жилье
    description = models.TextField(
        verbose_name='описание жилья',
        max_length=500,
        blank=True,
    )
    # шаг 10: Установите цену
    price = models.IntegerField(
        verbose_name='цена',
        blank=True,
        null=True,
    )
    # Проверить объявление: вывод общей формы (всю информацию) на одной странице

    hidden_fields = ['stage']
    required_fields = [
        'housing',
        'housing_type',
        'offer_type',
        'location',
        'guests',
        'beds',
        'bathroom',
        'photo1',
        'photo2',
        'photo3',
        'photo4',
        'photo5',
        'housing_header',
        'housing_description',
        'price',
    ]

    @staticmethod
    def get_fields_by_stage(stage):
        """Разбивает поля модели на группы по стадиям."""
        fields = ['stage']
        if stage == constants.STAGE_1:
            fields.extend(['housing'])
        elif stage == constants.STAGE_2:
            fields.extend(['housing_type'])
        elif stage == constants.STAGE_3:
            fields.extend(['offer_type'])
        elif stage == constants.STAGE_4:
            fields.extend(['location'])
        elif stage == constants.STAGE_5:
            fields.extend(['guests', 'beds', 'bathroom'])
        elif stage == constants.STAGE_6:
            fields.extend(['special_amenities', 'popular_amenities', 'safety'])
        elif stage == constants.STAGE_7:
            fields.extend(['photo1', 'photo2', 'photo3', 'photo4', 'photo5'])
        elif stage == constants.STAGE_8:
            fields.extend(['housing_header'])
        elif stage == constants.STAGE_9:
            fields.extend(['housing_description'])
        elif stage == constants.STAGE_10:
            fields.extend(['price'])
        return fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.session_hash:
            while True:
                session_hash = create_session_room_hash()
                if RoomsApplicationModel.objects.filter(session_hash=session_hash).count() == 0:
                    self.session_hash = session_hash
                    break

    def __str__(self):
        return self.header

    def get_absolute_url(self):
        return reverse('rooms:room_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'жилье'
        verbose_name_plural = 'жилье'
        ordering = ['-created_at']


class Reservation(models.Model):
    """Модель для создания брони жилья."""
    apartment = models.ForeignKey(
        RoomsApplicationModel,
        on_delete=models.CASCADE,
        related_name='apartment',
        verbose_name='бронируемое жилье',
    )
    start_date = models.DateField(
        verbose_name='прибытие',
    )
    end_date = models.DateField(
        verbose_name='выезд',
    )
    name_reserv = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='name_reserv',
        verbose_name='имя пользователя',
        blank=True,
    )
    days_total = models.IntegerField(
        verbose_name='всего дней',
        blank=True,
        null=True,
    )
    price_total = models.IntegerField(
        verbose_name='итоговая цена',
        blank=True,
        null=True,
    )
    status = models.BooleanField(
        verbose_name='Бронь подтверждена?',
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name='дата бронирования',
        auto_now_add=True,
    )

    def get_absolute_url(self):
        return reverse('rooms:room_reserv_details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.apartment.housing_header

    class Meta:
        verbose_name = 'резерв жилья'
        verbose_name_plural = 'резерв жилья'
        ordering = ['created_at']
