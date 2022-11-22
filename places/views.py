import json
import os
from typing import Dict, Any

from django.shortcuts import render
from django.conf import settings

from .models import Place


def write_json_by_place(place: Place) -> str:
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


def index(request):
    places_geojson = {
        'type': 'FeatureCollection',
        'features': [write_feature_by_place(place) for place in Place.objects.all()]
    }
    context = {'places_geojson': places_geojson}
    return render(request, 'index.html', context)
