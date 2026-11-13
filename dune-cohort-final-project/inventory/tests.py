from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Car, Manufacturer, Owner, ServiceRecord


class BaseTestCase(TestCase):
    def setUp(self):
        self.maker = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.owner = Owner.objects.create(full_name="Ada Obi")
        self.car = Car.objects.create(
            manufacturer=self.maker,
            owner=self.owner,
            model_name="Corolla",
            year=2020,
            color="White",
            price="15000.00",
            mileage=40000,
        )
        self.user = User.objects.create_user("sam", password="pass12345")
        self.staff = User.objects.create_user(
            "boss", password="pass12345", is_staff=True
        )

    def car_form_data(self, **overrides):
        data = {
            "manufacturer": self.maker.pk,
            "owner": "",
            "model_name": "Camry",
            "year": 2021,
            "color": "Black",
            "price": "22000.00",
            "mileage": 1000,
            "description": "",
        }
        data.update(overrides)
        return data


class ModelTests(BaseTestCase):
    def test_str_methods(self):
        self.assertEqual(str(self.maker), "Toyota")
        self.assertEqual(str(self.owner), "Ada Obi")
        self.assertEqual(str(self.car), "2020 Toyota Corolla")

    def test_deleting_manufacturer_cascades_to_cars_and_service_records(self):
        ServiceRecord.objects.create(
            car=self.car, service_date="2024-01-01", description="Oil", cost="50"
        )
        self.maker.delete()
        self.assertEqual(Car.objects.count(), 0)
        self.assertEqual(ServiceRecord.objects.count(), 0)

    def test_deleting_owner_keeps_car(self):
        self.owner.delete()
        self.car.refresh_from_db()
        self.assertIsNone(self.car.owner)


class PageTests(BaseTestCase):
    def test_public_pages_load(self):
        for name, args in [
            ("inventory:car_list", []),
            ("inventory:car_detail", [self.car.pk]),
            ("inventory:manufacturer_list", []),
            ("inventory:manufacturer_detail", [self.maker.pk]),
        ]:
            response = self.client.get(reverse(name, args=args))
            self.assertEqual(response.status_code, 200, name)

    def test_unknown_car_returns_404(self):
        response = self.client.get(reverse("inventory:car_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_create_requires_login(self):
        response = self.client.get(reverse("inventory:car_create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_create_car_redirects_and_flashes_message(self):
        self.client.login(username="sam", password="pass12345")
        response = self.client.post(
            reverse("inventory:car_create"), self.car_form_data(), follow=True
        )
        self.assertEqual(Car.objects.count(), 2)
        self.assertContains(response, "was added to the inventory")

    def test_create_rejects_future_year(self):
        self.client.login(username="sam", password="pass12345")
        response = self.client.post(
            reverse("inventory:car_create"), self.car_form_data(year=2999)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Car.objects.count(), 1)

    def test_update_car(self):
        self.client.login(username="sam", password="pass12345")
        url = reverse("inventory:car_update", args=[self.car.pk])
        response = self.client.post(url, self.car_form_data(color="Red"), follow=True)
        self.car.refresh_from_db()
        self.assertEqual(self.car.color, "Red")
        self.assertContains(response, "was updated")

    def test_non_staff_cannot_delete(self):
        self.client.login(username="sam", password="pass12345")
        self.client.post(reverse("inventory:car_delete", args=[self.car.pk]))
        self.assertTrue(Car.objects.filter(pk=self.car.pk).exists())

    def test_staff_can_delete(self):
        self.client.login(username="boss", password="pass12345")
        response = self.client.post(
            reverse("inventory:car_delete", args=[self.car.pk]), follow=True
        )
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())
        self.assertContains(response, "was deleted")

    def test_add_service_record(self):
        self.client.login(username="sam", password="pass12345")
        self.client.post(
            reverse("inventory:service_record_create", args=[self.car.pk]),
            {"service_date": "2024-01-01", "description": "Oil change", "cost": "40"},
        )
        self.assertEqual(self.car.service_records.count(), 1)


class RegistrationTests(TestCase):
    def test_register_logs_user_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "a-Strong-pass-123",
                "password2": "a-Strong-pass-123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())


class APITests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.api = APIClient()
        self.payload = {
            "manufacturer": self.maker.pk,
            "model_name": "Yaris",
            "year": 2019,
            "color": "Blue",
            "price": "9000.00",
            "mileage": 500,
        }

    def test_list_is_public(self):
        response = self.api.get("/api/cars/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_detail_and_404(self):
        self.assertEqual(self.api.get(f"/api/cars/{self.car.pk}/").status_code, 200)
        self.assertEqual(self.api.get("/api/cars/9999/").status_code, 404)

    def test_unauthenticated_write_is_rejected(self):
        response = self.api.post("/api/cars/", self.payload, format="json")
        self.assertEqual(response.status_code, 401)

    def test_create_returns_201(self):
        self.api.force_authenticate(self.user)
        response = self.api.post("/api/cars/", self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["manufacturer_name"], "Toyota")

    def test_invalid_create_returns_400(self):
        self.api.force_authenticate(self.user)
        response = self.api.post("/api/cars/", {"model_name": "x"}, format="json")
        self.assertEqual(response.status_code, 400)

    def test_delete_returns_204(self):
        self.api.force_authenticate(self.user)
        response = self.api.delete(f"/api/cars/{self.car.pk}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())
