from django.db import models
from django.urls import reverse


def localities_photo_upload_to(instance, filename):
    """Динамический путь для сохранения изображений населенных пунктов."""
    return f'photos/{instance.title}/{instance.title}/{filename}'


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
    photo = models.ImageField(
        verbose_name='изображение',
        upload_to=localities_photo_upload_to,
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


def intresting_place_photo_upload_to(instance, filename):
    """Динамический путь для сохранения изображений интересных мест."""
    return f'photos/{instance.category}/{instance.title}/{filename}'


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
    photo = models.ImageField(
        verbose_name='изображение',
        upload_to=intresting_place_photo_upload_to,
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