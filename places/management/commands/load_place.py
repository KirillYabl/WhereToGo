import uuid

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
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

    def upload_images(self, place, place_raw):
        for image_order, image_url in enumerate(place_raw['imgs'], start=1):
            self.upload_image(place, image_url, image_order)

    def load_place(self, url, force_update):
        response = requests.get(url)
        response.raise_for_status()
        place_raw = response.json()
        lat = place_raw['coordinates']['lat']
        lon = place_raw['coordinates']['lng']

        place_with_same_title_set = Place.objects.filter(title=place_raw['title'])

        # if 0 then anyway create new, if more than 1 then don't know what to update
        update_place = False
        if place_with_same_title_set.count() == 1:
            place_with_same_title = place_with_same_title_set.first()
            same_lat_lon = place_with_same_title.lat == float(lat) and \
                           place_with_same_title.lon == float(lon)

            update_message = '''You have place with the same title{adding}.
Enter `y` if you want to update it, otherwise it will create new one.
'''
            adding = ', latitude and longitude' if same_lat_lon else ''
            update_message = update_message.format(adding=adding)
            update_place = force_update or input(update_message).lower() == 'y'

        update_data = {
            'lat': lat,
            'lon': lon,
            'description_short': place_raw['description_short'],
            'description_long': place_raw['description_long'],
        }
        create_data = update_data.copy()
        create_data['title'] = place_raw['title']
        if update_place:
            Place.objects.filter(pk=place_with_same_title.pk).update(**update_data)
            PlaceImage.objects.filter(place__pk=place_with_same_title.pk).delete()
            self.upload_images(place_with_same_title, place_raw)

            print('Place was successfully updated')
            return

        place = Place(**create_data)
        place.save()
        self.upload_images(place, place_raw)
        print('Place was successfully created')
        return

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
