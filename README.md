# My Cloud & Data Storage Web App

This project now includes a **full-stack web page** where you can manage your own cloud data records.

## Features

- Add cloud data records (title, data type, storage region, description)
- Store records in a local SQLite database
- View saved records in a dashboard
- Delete records from the UI

## Tech Stack

- Backend: Python + Flask
- Database: SQLite (`cloud_data.db`)
- Frontend: HTML, CSS, Vanilla JavaScript

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open: `http://127.0.0.1:5000`

## API Endpoints

- `GET /api/records` → list records
- `POST /api/records` → create a record
- `DELETE /api/records/<id>` → delete a record
