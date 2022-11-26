from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Place
from . import utils


def get_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    return JsonResponse(
        utils.construct_dict_by_place(place),
        json_dumps_params={'ensure_ascii': False, 'indent': 4}
    )


def index(request):
    places_geojson = {
        'type': 'FeatureCollection',
        'features': [utils.write_feature_by_place(place) for place in Place.objects.all()]
    }
    context = {'places_geojson': places_geojson}
    return render(request, 'index.html', context)
