from django.contrib import admin

from .models import Car, Manufacturer, Owner, ServiceRecord


class ServiceRecordInline(admin.TabularInline):
    model = ServiceRecord
    extra = 0


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "founded_year")
    search_fields = ("name", "country")


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone")
    search_fields = ("full_name", "email")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("__str__", "color", "price", "mileage", "owner")
    list_filter = ("manufacturer", "year")
    search_fields = ("model_name", "manufacturer__name")
    inlines = [ServiceRecordInline]


@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ("car", "service_date", "description", "cost")
    list_filter = ("service_date",)
