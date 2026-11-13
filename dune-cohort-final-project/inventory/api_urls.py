from django.urls import path

from . import api_views

urlpatterns = [
    path("cars/", api_views.CarListCreateAPIView.as_view(), name="api_car_list"),
    path("cars/<int:pk>/", api_views.CarDetailAPIView.as_view(), name="api_car_detail"),
]
