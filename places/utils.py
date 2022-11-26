from typing import Dict, Any

from django.urls import reverse

from .models import Place


def construct_dict_by_place(place: Place) -> Dict[str, Any]:
    return {
        'title': place.title,
        'imgs': [image.place_image.url for image in place.images.all()],
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coordinates': {
            'lng': place.lon,
            'lat': place.lat
        }
    }


def write_feature_by_place(place: Place) -> Dict[str, Any]:
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [place.lon, place.lat]
        },
        'properties': {
            'title': place.title,
            'placeId': place.pk,
            'detailsUrl': reverse('place', kwargs={'place_pk': place.pk})
        }
    }
    return feature
