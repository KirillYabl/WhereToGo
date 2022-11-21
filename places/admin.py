from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    pass
