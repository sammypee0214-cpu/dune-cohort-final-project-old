# Dune Garage - Car Inventory

Dune Cohort · Backend Development with Python & Django · Module 16 Final Project

## Live site

**https://YOUR-APP.onrender.com**  <!-- replace with your real Render URL -->

- Admin: `/admin/`
- REST API: `/api/cars/`

## What it does

A car inventory manager. Visitors can browse and search cars. Registered users
can add and edit cars and log service records. Only staff users can delete cars.

## Apps and models

| App | Responsibility |
| --- | --- |
| `inventory` | Models, pages, CRUD, REST API |
| `accounts` | Registration, login, logout |

| Model | Relationships |
| --- | --- |
| `Manufacturer` | Has many `Car` |
| `Owner` | Has many `Car` (`SET_NULL`) |
| `Car` | FK to `Manufacturer` (`CASCADE`), FK to `Owner` (`SET_NULL`), has an `ImageField` |
| `ServiceRecord` | FK to `Car` (`CASCADE`) |

## Pages

| URL | Page | Access |
| --- | --- | --- |
| `/` | Car list (search + filter) | Public |
| `/cars/<pk>/` | Car detail + service history | Public |
| `/cars/add/` | Create car | Login required |
| `/cars/<pk>/edit/` | Edit car | Login required |
| `/cars/<pk>/delete/` | Delete car | Staff only |
| `/cars/<pk>/service/add/` | Add service record | Login required |
| `/manufacturers/` | Manufacturer list | Public |
| `/manufacturers/<pk>/` | Manufacturer + its cars | Public |
| `/accounts/register/`, `/accounts/login/` | Auth | Public |

## REST API

| Method | Endpoint | Auth | Success | Errors |
| --- | --- | --- | --- | --- |
| GET | `/api/cars/` | No | 200 | |
| POST | `/api/cars/` | Yes | 201 | 400, 401 |
| GET | `/api/cars/<id>/` | No | 200 | 404 |
| DELETE | `/api/cars/<id>/` | Yes | 204 | 401, 404 |

`PUT`/`PATCH` on `/api/cars/<id>/` are also available (auth required). Auth is
HTTP Basic (username and password) or a logged-in session.

The Postman collection is in [`postman/dune-garage-api.postman_collection.json`](postman/dune-garage-api.postman_collection.json).
Import it, set the `base_url`, `username` and `password` collection variables,
then run the collection in order.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export DEBUG=True                  # Windows PowerShell: $env:DEBUG="True"
python manage.py migrate
python manage.py seed_demo         # starter manufacturers
python manage.py createsuperuser
python manage.py runserver
```

Run the tests with `DEBUG=True python manage.py test`.

## Deploy on Render

1. Create a **PostgreSQL** database on Render and copy its *Internal Database URL*.
2. Create a **Web Service** from this GitHub repo with:
   - Build command: `bash build.sh`
   - Start command: `gunicorn config.wsgi:application`
3. Add environment variables:

   | Key | Value |
   | --- | --- |
   | `SECRET_KEY` | a long random string |
   | `DEBUG` | `False` |
   | `DATABASE_URL` | the Internal Database URL from step 1 |
   | `DJANGO_SUPERUSER_USERNAME` / `DJANGO_SUPERUSER_EMAIL` / `DJANGO_SUPERUSER_PASSWORD` | optional, creates an admin on first deploy |

4. Deploy, then visit your `https://...onrender.com` URL.

`build.sh` installs dependencies, runs `collectstatic` (served by WhiteNoise),
applies migrations and seeds demo manufacturers.

### Known limitation

Render's free web services have an ephemeral disk, so car photos uploaded
through the site are lost on redeploy. Production use would need object storage
such as S3 or Cloudinary.
