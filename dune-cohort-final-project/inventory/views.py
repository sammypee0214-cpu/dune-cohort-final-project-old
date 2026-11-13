"""Template-rendered pages for the Dune Garage inventory."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CarForm, ServiceRecordForm
from .models import Car, Manufacturer


def car_list(request):
    """Home page: all cars, with optional text search and manufacturer filter."""
    cars = Car.objects.select_related("manufacturer", "owner")

    query = request.GET.get("q", "").strip()
    maker_id = request.GET.get("manufacturer", "")

    if query:
        cars = cars.filter(
            Q(model_name__icontains=query) | Q(manufacturer__name__icontains=query)
        )
    if maker_id.isdigit():
        cars = cars.filter(manufacturer_id=int(maker_id))

    context = {
        "cars": cars,
        "manufacturers": Manufacturer.objects.all(),
        "query": query,
        "selected_maker": maker_id,
    }
    return render(request, "inventory/car_list.html", context)


def car_detail(request, pk):
    """Single car with its service history (dynamic URL: /cars/<pk>/)."""
    car = get_object_or_404(
        Car.objects.select_related("manufacturer", "owner").prefetch_related(
            "service_records"
        ),
        pk=pk,
    )
    return render(request, "inventory/car_detail.html", {"car": car})


@login_required
def car_create(request):
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save()
            messages.success(request, f"{car} was added to the inventory.")
            return redirect(car)  # redirect after POST
    else:
        form = CarForm()
    return render(
        request, "inventory/car_form.html", {"form": form, "heading": "Add a car"}
    )


@login_required
def car_update(request, pk):
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save()
            messages.success(request, f"{car} was updated.")
            return redirect(car)
    else:
        form = CarForm(instance=car)
    return render(
        request,
        "inventory/car_form.html",
        {"form": form, "heading": f"Edit {car}", "car": car},
    )


@login_required
def car_delete(request, pk):
    """Delete a car. Restricted to staff users only."""
    car = get_object_or_404(Car, pk=pk)

    if not request.user.is_staff:
        messages.error(request, "Only staff members can delete cars.")
        return redirect(car)

    if request.method == "POST":
        label = str(car)
        car.delete()
        messages.success(request, f"{label} was deleted.")
        return redirect("inventory:car_list")
    return render(request, "inventory/car_confirm_delete.html", {"car": car})


@login_required
def service_record_create(request, pk):
    """Add a service record to a car (dynamic URL: /cars/<pk>/service/add/)."""
    car = get_object_or_404(Car, pk=pk)
    if request.method == "POST":
        form = ServiceRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.car = car
            record.save()
            messages.success(request, "Service record added.")
            return redirect(car)
    else:
        form = ServiceRecordForm()
    return render(
        request, "inventory/service_form.html", {"form": form, "car": car}
    )


def manufacturer_list(request):
    manufacturers = Manufacturer.objects.annotate(car_count=Count("cars"))
    return render(
        request, "inventory/manufacturer_list.html", {"manufacturers": manufacturers}
    )


def manufacturer_detail(request, pk):
    """Manufacturer page listing its cars (dynamic URL: /manufacturers/<pk>/)."""
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    return render(
        request,
        "inventory/manufacturer_detail.html",
        {"manufacturer": manufacturer, "cars": manufacturer.cars.all()},
    )
