from django.contrib import admin

from .models import Localities, InterestingPlaces


class LocalitiesAdmin(admin.ModelAdmin):
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
        'photo',
        'created_at',
        'updated_at',
        'is_published',
        'views',
    )
    readonly_fields = ('created_at', 'updated_at', 'views')


class InterestingPlacesAdmin(admin.ModelAdmin):
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
        'photo',
        'created_at',
        'updated_at',
        'is_published',
        'views',
    )
    readonly_fields = ('created_at', 'updated_at', 'views')
    save_on_top = True


admin.site.register(Localities, LocalitiesAdmin)
admin.site.register(InterestingPlaces, InterestingPlacesAdmin)