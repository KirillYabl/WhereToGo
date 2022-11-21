from django.db import models


# Create your models here.
class Place(models.Model):
    title = models.CharField(verbose_name='название', max_length=500)
    description_short = models.TextField(verbose_name='краткое описание')
    description_long = models.TextField(verbose_name='полное описание', blank=True, null=True)
    lat = models.FloatField(verbose_name='широта')
    lon = models.FloatField(verbose_name='долгота')

    def __str__(self):
        return self.title
