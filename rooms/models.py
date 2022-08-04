from django.urls import reverse
from django.db import models
from django.db.models import Avg

from django.contrib.auth import get_user_model
User = get_user_model()


def rooms_photo_upload_to(instance, filename):
    return f'rooms/{instance.landlord}/{instance.id}/{filename}'


class RoomsModel(models.Model):
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
    landlord = models.ForeignKey(
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
    housing = models.CharField(
        verbose_name='какое у вас жилье?',
        max_length=100,
        blank=True,
    )
    housing_type = models.CharField(
        verbose_name='что из перечисленного точнее описывает ваше жилье?',
        max_length=100,
        blank=True,
    )
    offer_type = models.CharField(
        verbose_name='что вы предлагаете?',
        max_length=100,
        blank=True,
    )
    location = models.CharField(
        verbose_name='где расположено ваше жилье?',
        max_length=255,
        blank=True,
    )
    map_location = models.TextField(
        verbose_name='расположение на карте',
        blank=True
    )
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
    header = models.CharField(
        verbose_name='придумайте яркое название жилья',
        max_length=50,
        blank=True,
    )
    description = models.TextField(
        verbose_name='описание жилья',
        max_length=500,
        blank=True,
    )
    price = models.IntegerField(
        verbose_name='цена',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.header

    def get_reviews(self):
        """Возвращает список отзывов жилья."""
        return self.reviews_set.filter(status=True).order_by('-id')

    def get_ratings(self):
        """Возвращает среднюю оценку жилья."""
        return self.rating_set.filter(status=True).aggregate(Avg('star'))

    def get_absolute_url(self):
        return reverse('rooms:room_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'жилье'
        verbose_name_plural = 'жилье'
        ordering = ['-created_at']


class Reservation(models.Model):
    """Модель для создания брони жилья."""
    apartment = models.ForeignKey(
        RoomsModel,
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='name_reserv',
        verbose_name='имя пользователя',
        blank=True,
    )
    guests = models.PositiveSmallIntegerField(
        verbose_name='гостей'
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
        return self.apartment.housing

    class Meta:
        verbose_name = 'резерв жилья'
        verbose_name_plural = 'резерв жилья'
        ordering = ['start_date']


class RatingStar(models.Model):
    """Звезды оценки."""
    value = models.SmallIntegerField('значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'звезда оценки'
        verbose_name_plural = 'звезды оценки'
        ordering = ['-value']


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    apartment = models.ForeignKey(
        RoomsModel,
        on_delete=models.CASCADE,
        verbose_name='жилье',
    )
    star = models.ForeignKey(
        RatingStar,
        on_delete=models.CASCADE,
        verbose_name='звезда',
    )
    status = models.BooleanField(
        default=True,
        verbose_name='опубликован?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания',
    )

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'


class Reviews(models.Model):
    """Отзывы."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь',
    )
    apartment = models.ForeignKey(
        RoomsModel,
        on_delete=models.CASCADE,
        verbose_name='жилье',
    )
    review = models.TextField(
        max_length=500,
        verbose_name='отзыв',
        blank=True,
    )
    status = models.BooleanField(
        default=True,
        verbose_name='опубликован?'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания',
    )

    def __str__(self):
        return f'{self.user_review} - {self.apartment}'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-created_at']
