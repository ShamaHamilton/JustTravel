from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Localities, LocalityImages, Places, PlaceImages


class LocalitiesAdminForm(forms.ModelForm):
    """Подключение CKEditor к форме модели."""
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Localities
        fields = '__all__'


class LocalitiesAdmin(admin.ModelAdmin):
    """Населенные пункты."""
    form = LocalitiesAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'id',
        'title',
        'created_at',
        'updated_at',
        'is_published',
        'views',
    )
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_filter = ('is_published',)
    fields = (
        'title',
        'slug',
        'content',
        'preview',
        'created_at',
        'updated_at',
        'is_published',
        'views',
    )
    readonly_fields = ('created_at', 'updated_at', 'views')


admin.site.register(Localities, LocalitiesAdmin)


class PlacesAdminForm(forms.ModelForm):
    """Подключение CKEditor к форме модели."""
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Places
        fields = '__all__'


class PlacesAdmin(admin.ModelAdmin):
    """Интересные места."""
    form = PlacesAdminForm
    prepopulated_fields = {'slug': ('title',)}
    save_as = True
    list_display = (
        'id',
        'title',
        'category',
        'created_at',
        'updated_at',
        'is_published',
        'views',
    )
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('is_published', 'category')
    fields = (
        'title',
        'slug',
        'category',
        'content',
        'preview',
        'created_at',
        'updated_at',
        'is_published',
        'views',
    )
    readonly_fields = ('created_at', 'updated_at', 'views')
    save_on_top = True


admin.site.register(Places, PlacesAdmin)


class LocalityImagesAdmin(admin.ModelAdmin):
    """Изображения населенных пунктов."""
    list_display = ('id', 'category', 'get_photo',)
    list_display_links = ('category',)
    search_fields = ('category',)
    list_filter = ('category',)
    fields = ('category', 'get_photo', 'photo',)
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')

    get_photo.short_description = 'миниатюра'


admin.site.register(LocalityImages, LocalityImagesAdmin)


class PlaceImagesAdmin(admin.ModelAdmin):
    """Изображения интересных мест."""
    list_display = ('id', 'category_place', 'get_photo',)
    list_display_links = ('category_place',)
    search_fields = ('category_place',)
    list_filter = ('category_place',)
    fields = ('category_place', 'get_photo', 'photo',)
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')

    get_photo.short_description = 'миниатюра'


admin.site.register(PlaceImages, PlaceImagesAdmin)
