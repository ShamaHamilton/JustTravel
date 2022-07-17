from django.shortcuts import render

from .models import Localities, LocalityImages, InterestingPlaces, PlaceImages
from rooms.models import RoomsApplicationModel


def home(request):
    places_view = InterestingPlaces.objects.filter(is_published=True)
    localities_view = Localities.objects.filter(is_published=True)
    context = {
        'places_view': places_view,
        'localities_view': localities_view,
    }
    return render(request, 'blogs/home.html', context)


def localities_list_view(request):
    localities_list = Localities.objects.filter(is_published=True)
    context = {
        'localities_list': localities_list,
    }
    return render(request, 'blogs/locality_list.html', context)

# ! Добавить счетчик просмотров.
def locality_detail_view(request, slug):
    locality = Localities.objects.get(slug=slug)
    locality.views += 1
    locality.save()
    context = {
        'locality': locality,
    }
    return render(request, 'blogs/locality_detail.html', context)


def places_list_view(request):
    places_list = InterestingPlaces.objects.filter(is_published=True)
    context = {
        'places_list': places_list,
    }
    return render(request, 'blogs/places_list.html', context)


# ! Добавить счетчик просмотров.
def place_detail_view(request, slug):
    place = InterestingPlaces.objects.get(slug=slug)
    place.views += 1
    place.save()
    context = {
        'place': place,
    }
    return render(request, 'blogs/place_detail.html', context)