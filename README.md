# Mechanic Board

This project now supports a simple local deployment path and a small JSON API for future mobile clients.

## Run locally

From the repository root:

```bash
cd app
DB_ENGINE=sqlite3 /bin/python manage.py migrate
DB_ENGINE=sqlite3 /bin/python manage.py runserver 0.0.0.0:8000
```

Or use the deployment script:

```bash
bash scripts/deploy.sh
```

## API endpoints

- GET /api/workorders/
- GET /api/workorders/<id>/
- PATCH /api/workorders/<id>/

This is a good base for a future Android app that can view and update work orders.
