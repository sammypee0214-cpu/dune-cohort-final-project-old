from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.car_list, name="car_list"),
    path("cars/add/", views.car_create, name="car_create"),
    path("cars/<int:pk>/", views.car_detail, name="car_detail"),
    path("cars/<int:pk>/edit/", views.car_update, name="car_update"),
    path("cars/<int:pk>/delete/", views.car_delete, name="car_delete"),
    path(
        "cars/<int:pk>/service/add/",
        views.service_record_create,
        name="service_record_create",
    ),
    path("manufacturers/", views.manufacturer_list, name="manufacturer_list"),
    path(
        "manufacturers/<int:pk>/",
        views.manufacturer_detail,
        name="manufacturer_detail",
    ),
]
