from rest_framework import serializers

from .models import Car


class CarSerializer(serializers.ModelSerializer):
    # Read-only convenience field so API clients see the name, not just the id.
    manufacturer_name = serializers.CharField(
        source="manufacturer.name", read_only=True
    )

    class Meta:
        model = Car
        fields = [
            "id",
            "manufacturer",
            "manufacturer_name",
            "owner",
            "model_name",
            "year",
            "color",
            "price",
            "mileage",
            "description",
            "image",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
