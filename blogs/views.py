from django.shortcuts import render

from .models import Localities, LocalityImages, InterestingPlaces, PlaceImages
from rooms.models import RoomsApplicationModel


def home(request):
    places_view = InterestingPlaces.objects.filter(is_published=True)
    localities_view = Localities.objects.filter(is_published=True)
    rooms_view = RoomsApplicationModel.objects.filter(status=True)
    context = {
        'places_view': places_view,
        'localities_view': localities_view,
        'rooms_view': rooms_view,
    }
    return render(request, 'blogs/home.html', context)


def localities_view(request):
    localities_list = Localities.objects.filter(is_published=True)
    places_list = InterestingPlaces.objects.filter(is_published=True)
    context = {
        'localities_list': localities_list,
        'places_list': places_list,
    }
    return render(request, 'blogs/locality_list.html', context)

# ! Добавить счетчик просмотров.
def locality_detail_view(request, slug):
    locality = Localities.objects.get(slug=slug)
    images = LocalityImages.objects.filter(category_id=locality.pk)
    context = {
        'locality': locality,
        'images': images,
    }
    return render(request, 'blogs/locality_detail.html', context)


def places_view(request):
    places_list = InterestingPlaces.objects.filter(is_published=True)
    context = {
        'places_list': places_list,
    }
    return render(request, 'blogs/places_list.html', context)


# ! Добавить счетчик просмотров.
def place_detail_view(request, slug):
    place = InterestingPlaces.objects.get(slug=slug)
    images = PlaceImages.objects.filter(category_place_id=place.pk)
    context = {
        'place': place,
        'images': images,
    }
    return render(request, 'blogs/place_detail.html', context)