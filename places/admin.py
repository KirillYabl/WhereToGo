from django.contrib import admin
from . import models


class PlaceImageInline(admin.TabularInline):
    model = models.PlaceImage


# Register your models here.
@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [PlaceImageInline, ]


@admin.register(models.PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    pass
