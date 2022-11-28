import uuid

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
import requests

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Load location by url or locations by file with urls'

    @staticmethod
    def upload_image(place, image_url, image_order):
        response = requests.get(image_url)
        response.raise_for_status()
        content_file = ContentFile(response.content, name=str(uuid.uuid4()))
        place_image = PlaceImage.objects.create(place=place, place_image=content_file, image_order=image_order)
        place_image.save()

    def load_place(self, url, force_update):
        response = requests.get(url)
        response.raise_for_status()
        place_raw = response.json()
        lat = place_raw['coordinates']['lat']
        lon = place_raw['coordinates']['lng']

        defaults = {
            'description_short': place_raw.get('description_short', ''),
            'description_long': place_raw.get('description_long', ''),
        }

        if force_update:
            place, created = Place.objects.update_or_create(title=place_raw['title'], lat=lat, lon=lon,
                                                            defaults=defaults)
        else:
            place, created = Place.objects.get_or_create(title=place_raw['title'], lat=lat, lon=lon,
                                                         defaults=defaults)
            if not created:
                print(
                    'Place with same title, lat and lon already exists. Use flag --force_update if you want update it.')
                print(f'Place {place} skipped')
                return

        # if place need to update is is needs to delete old images
        if not created and force_update:
            PlaceImage.objects.filter(place__pk=place.pk).delete()

        images_links = place_raw.get('imgs', [])
        if not images_links:
            print(f'WARNING: place "{place}" do not have images')
        for image_order, image_url in enumerate(images_links, start=1):
            self.upload_image(place, image_url, image_order)

        if created and not force_update:
            print(f'Place {place} was successfully created')
            return

        print(f'Place {place} was successfully updated')

    def add_arguments(self, parser):
        parser.add_argument('url_or_path', type=str,
                            help='URL of place or path to file with urls (use -f flag for the second variant)')
        parser.add_argument('-fu', '--force_update', help='Update if exists', action='store_true')
        parser.add_argument('-f', '--file', help='Update many from file with links', action='store_true')

    def handle(self, *args, **options):
        url_or_path = options['url_or_path']
        force_update = options['force_update']
        is_file = options['file']

        urls = [url_or_path]
        if is_file:
            with open(url_or_path) as f:
                urls = [url.strip() for url in f.readlines()]

        for url in urls:
            self.load_place(url, force_update)
