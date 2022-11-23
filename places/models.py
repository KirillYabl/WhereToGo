from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class Place(models.Model):
    title = models.CharField(verbose_name='название', max_length=500)
    description_short = models.TextField(verbose_name='краткое описание')
    description_long = HTMLField(verbose_name='полное описание', blank=True, null=True)
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'


class PlaceImage(models.Model):
    place = models.ForeignKey(to=Place, related_name='images', on_delete=models.CASCADE)
    place_image = models.ImageField(verbose_name='картинка места')
    image_order = models.PositiveSmallIntegerField(verbose_name='порядок отображения',
                                                   help_text='порядок от меньшего к большему, т.е. 1 покажется первой')

    def __str__(self):
        return f'{self.image_order} {self.place_image.path}'

    class Meta:
        verbose_name = 'изображение места'
        verbose_name_plural = 'изображения места'
        ordering = ['image_order']
