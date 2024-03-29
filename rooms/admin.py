from django.contrib import admin
from django import forms

from .models import RoomsModel, Reservation,RatingStar, Rating, Reviews


class RoomsCreationForm(forms.ModelForm):
    """Форма для создания жилья из админки."""

    class Meta:
        model = RoomsModel
        fields = '__all__'


class RoomsChangeForm(forms.ModelForm):
    """Форма для редактирования пользовательских параметров."""

    class Meta:
        model = RoomsModel
        fields = (
            'landlord',
            'status',
            'header',
            'description',
            'housing',
            'housing_type',
            'offer_type',
            'location',
            'map_location',
            'guests',
            'beds',
            'bathroom',
            'special_amenities',
            'popular_amenities',
            'safety',
            'photo1',
            'photo2',
            'photo3',
            'photo4',
            'photo5',
            'price',
        )


class RoomsAdmin(admin.ModelAdmin):
    """Форма для добавления и изменения пользовательских экземпляров."""
    form = RoomsCreationForm
    add_form = RoomsChangeForm
    list_display = (
        'id',
        'landlord',
        'status',
        'housing',
        'header',
        'offer_type',
        'price',
        'views',
    )
    list_display_links = ('id', 'landlord')
    search_fields = ('landlord',)
    list_editable = ('status',)
    list_filter = ('landlord', 'status')
    fields = (
        'landlord',
        'status',
        'header',
        'description',
        'housing',
        'housing_type',
        'offer_type',
        'location',
        'map_location',
        'guests',
        'beds',
        'bathroom',
        'special_amenities',
        'popular_amenities',
        'safety',
        'photo1',
        'photo2',
        'photo3',
        'photo4',
        'photo5',
        'price',
        'views',
        'created_at',
        'updated_at',
    )
    readonly_fields = ('created_at', 'updated_at')
    save_on_top = True


admin.site.register(RoomsModel, RoomsAdmin)


class ReservationForm(forms.ModelForm):
    """Форма для создания жилья из админки."""

    class Meta:
        model = RoomsModel
        fields = '__all__'
        exclude = ('created_at',)


class ReservationAdmin(admin.ModelAdmin):
    """Форма для добавления и изменения пользовательских экземпляров."""
    list_display = (
        'id',
        'user',
        'apartment',
        'status',
        'start_date',
        'end_date',
        'guests',
        'days_total',
        'price_total',
    )
    list_display_links = ('id', 'user', 'apartment',)
    # search_fields = ('apartment',)
    list_editable = ('status',)
    list_filter = ('apartment', 'status')
    fields = (
        'apartment',
        'start_date',
        'end_date',
        'user',
        'guests',
        'days_total',
        'price_total',
        'status',
    )
    # save_on_top = True


admin.site.register(Reservation, ReservationAdmin)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Оценки."""
    list_display = ('star', 'apartment', 'user', 'status')


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы."""
    list_display = (
        'id',
        'user',
        'apartment',
        'review',
        'status',
        'created_at',
    )
    list_display_links = ('id', 'user',)
    search_fields = ('apartment',)
    list_filter = ('apartment',)
    fields = (
        'user',
        'apartment',
        'review',
        'status',
        'created_at',
    )
    readonly_fields = ('created_at',)


admin.site.register(RatingStar)
