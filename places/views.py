import json
import os
from typing import Dict, Any

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Place


def construct_json_by_place(place: Place) -> Dict[str, Any]:
    json_file_data = {
        "title": place.title,
        "imgs": [image.place_image.url for image in place.images.all()],
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lon,
            "lat": place.lat
        }
    }
    return json_file_data


def write_json_by_place(place: Place) -> str:
    json_file_data = construct_json_by_place(place)
    filename = f'{place.pk}.json'
    with open(os.path.join(settings.MEDIA_ROOT, filename), 'w', encoding='UTF-8') as f:
        json.dump(json_file_data, f, ensure_ascii=False)

    return f"./media/{filename}"


def write_feature_by_place(place: Place) -> Dict[str, Any]:
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [place.lon, place.lat]
        },
        "properties": {
            "title": place.title,
            "placeId": place.pk,
            "detailsUrl": write_json_by_place(place)
        }
    }
    return feature


def get_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    return JsonResponse(
        construct_json_by_place(place),
        json_dumps_params={'ensure_ascii': False, 'indent': 4}
    )


def index(request):
    places_geojson = {
        'type': 'FeatureCollection',
        'features': [write_feature_by_place(place) for place in Place.objects.all()]
    }
    context = {'places_geojson': places_geojson}
    return render(request, 'index.html', context)
