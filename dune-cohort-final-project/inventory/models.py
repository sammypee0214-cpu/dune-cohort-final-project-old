"""
Data model for the Dune Garage car inventory.

Relationships:
    Manufacturer 1 ---< Car          (ForeignKey, CASCADE)
    Owner        1 ---< Car          (ForeignKey, SET_NULL - a car can be unowned)
    Car          1 ---< ServiceRecord (ForeignKey, CASCADE)
"""
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    founded_year = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("inventory:manufacturer_detail", args=[self.pk])


class Owner(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class Car(models.Model):
    # Deleting a manufacturer removes all of its cars.
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, related_name="cars"
    )
    # Deleting an owner keeps the car, it just becomes unowned.
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cars",
    )
    model_name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1886)])
    color = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    mileage = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="cars/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.year} {self.manufacturer.name} {self.model_name}"

    def get_absolute_url(self):
        return reverse("inventory:car_detail", args=[self.pk])


class ServiceRecord(models.Model):
    # Deleting a car removes its service history.
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name="service_records"
    )
    service_date = models.DateField()
    description = models.CharField(max_length=255)
    cost = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(Decimal("0"))]
    )

    class Meta:
        ordering = ["-service_date"]

    def __str__(self):
        return f"{self.description} ({self.service_date}) - {self.car}"
