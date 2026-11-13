from datetime import date

from django import forms

from .models import Car, ServiceRecord


class CarForm(forms.ModelForm):
    """Create/edit form for cars, with extra validation on year and mileage."""

    class Meta:
        model = Car
        fields = [
            "manufacturer",
            "owner",
            "model_name",
            "year",
            "color",
            "price",
            "mileage",
            "description",
            "image",
        ]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def clean_year(self):
        year = self.cleaned_data["year"]
        latest = date.today().year + 1  # allow next year's models
        if year > latest:
            raise forms.ValidationError(f"Year cannot be later than {latest}.")
        return year

    def clean_mileage(self):
        mileage = self.cleaned_data["mileage"]
        if mileage > 2_000_000:
            raise forms.ValidationError("Mileage looks unrealistic. Please check it.")
        return mileage


class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ["service_date", "description", "cost"]
        widgets = {"service_date": forms.DateInput(attrs={"type": "date"})}

    def clean_service_date(self):
        service_date = self.cleaned_data["service_date"]
        if service_date > date.today():
            raise forms.ValidationError("Service date cannot be in the future.")
        return service_date
