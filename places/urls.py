from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('places/<int:place_pk>/', views.get_place, name='place'),
]
