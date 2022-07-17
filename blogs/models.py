from django.db import models
from django.urls import reverse


class Localities(models.Model):
    """Населенные пункты."""
    title = models.CharField(
        verbose_name='название',
        max_length=200,
        db_index=True,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='URL',
        max_length=255,
        unique=True,
    )
    content = models.TextField(
        verbose_name='содержание',
        blank=True,
    )
    # photo = models.ImageField(
    #     verbose_name='изображение',
    #     upload_to=localities_photo_upload_to,
    #     blank=True,
    # )
    created_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='дата редактирования',
        auto_now=True,
    )
    is_published = models.BooleanField(
        verbose_name='опубликовано ?',
        default=False,
    )
    views = models.IntegerField(
        verbose_name='количество просмотров',
        default=0,
    )

    # TODO: добавить метку на карте

    def get_absolute_url(self):
        """Возвращает URL объекта Localities."""
        return reverse('blogs:locality', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'населенный пункт'
        verbose_name_plural = 'населенные пункты'
        ordering = ['title']


def localities_photo_upload_to(instance, filename):
    """Динамический путь для сохранения изображений населенных пунктов."""
    return f'photos/{instance.category.title}/{instance.category.title}/{filename}'


class LocalityImages(models.Model):
    category = models.ForeignKey(
        Localities,
        on_delete=models.CASCADE,
        verbose_name='населенный пункт',
        related_name='image',
    )
    photo = models.ImageField(
        verbose_name='изображение',
        upload_to=localities_photo_upload_to,
    )

    def __str__(self):
        return self.category.title

    class Meta:
        verbose_name = 'изображение населенного пункта'
        verbose_name_plural = 'изображения населенных пунктов'
        ordering = ['category']


class InterestingPlaces(models.Model):
    """Интересные места."""
    title = models.CharField(
        verbose_name='заголовок',
        max_length=200,
        db_index=True,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='URL',
        max_length=255,
        unique=True,
    )
    content = models.TextField(
        verbose_name='содержание',
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='дата создания',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='дата редактирования',
        auto_now=True,
    )
    is_published = models.BooleanField(
        verbose_name='опубликовано ?',
        default=False,
    )
    category = models.ForeignKey(
        Localities,
        on_delete=models.PROTECT,
        related_name='places',
        verbose_name='категория',
    )
    views = models.IntegerField(
        verbose_name='количество просмотров',
        default=0,
    )

    # TODO: добавить метку на карте

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Возвращает URL объекта InterestingPlaces."""
        return reverse('blogs:place', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'интересное место'
        verbose_name_plural = 'интересные места'
        ordering = ['title']


def intresting_place_photo_upload_to(instance, filename):
    """Динамический путь для сохранения изображений интересных мест."""
    return f'photos/{instance.category_place.category}/{instance.category_place.title}/{filename}'


class PlaceImages(models.Model):
    category_place = models.ForeignKey(
        InterestingPlaces,
        on_delete=models.CASCADE,
        verbose_name='место',
        related_name='image',
    )
    photo = models.ImageField(
        verbose_name='изображение',
        upload_to=intresting_place_photo_upload_to,
        blank=True,
    )

    def __str__(self):
        return self.category_place.title

    class Meta:
        verbose_name = 'изображение интересного места'
        verbose_name_plural = 'изображения интересных мест'
        ordering = ['category_place']