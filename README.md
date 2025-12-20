# Product Importer – Backend Assignment

This project is a Django-based web application that allows importing a large number of products from a CSV file into a PostgreSQL database, managing products through a web UI, and configuring webhooks.
It is designed to demonstrate scalable data ingestion, asynchronous processing, and clean backend architecture.

> ⚠️ Note: This application is built as an evaluation assignment. The focus is on architecture, correctness, and clarity rather than production hardening.

---

## 🚀 Features

### 1. CSV Product Import (Async)
- Upload CSV files containing up to 500,000 products
- Case-insensitive SKU handling (SKU is unique)
- Existing products are overwritten by SKU
- Import runs asynchronously using Celery
- Real-time progress updates in UI (polling-based)
- Clear status indicators: Pending, Processing, Completed, Failed

### 2. Product Management UI
- View products with pagination
- Filter by SKU, name, description, and active status
- Create, update, and delete products
- Inline editing via modal forms
- Confirmation dialogs for destructive actions

### 3. Bulk Delete
- Delete all products with a confirmation step
- Visual feedback during processing
- Success / failure notifications

### 4. Webhook Management
- Create, edit, enable/disable, delete webhooks
- Configure event types
- Test webhooks from the UI
- Displays response status code and response time
- Webhook delivery is handled asynchronously

---

## 🏗️ Architecture Overview

Browser → Django (Gunicorn) → PostgreSQL  
                             ↘ Redis (Upstash) → Celery

---

## 🧰 Tech Stack

- Backend: Django 6
- Async: Celery
- Broker: Redis (Upstash)
- Database: PostgreSQL
- Deployment: Render
- Frontend: HTML + Vanilla JS

---

## 🖥️ Local Development Setup

### Clone repository
```
git clone https://github.com/Swatej1502/Product_importer_fulfil.git
cd Product_importer_fulfil
```

### Create virtual environment
```
python -m venv venv
source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Environment variables (.env)
```
DEBUG=True
SECRET_KEY=local-dev-secret

DB_NAME=acme
DB_USER=acme
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Run migrations
```
python manage.py migrate
```

### Run services
Terminal 1:
```
redis-server
```

Terminal 2:
```
celery -A product_importer worker --pool=solo -l info
```

Terminal 3:
```
python manage.py runserver
```

---

## ☁️ Deployment Notes (Render)

- Web Service: Django + Gunicorn
- Database: Render PostgreSQL
- Redis: Upstash (TLS enabled)

### Free-tier limitation
Render free tier does not support background workers.
For demo purposes, the Celery worker runs in the same container as the web service.

Start command:
```
sh -c "celery -A product_importer worker --pool=solo -l info & gunicorn product_importer.wsgi"
```

### Required Environment Variables (Render)
```
DEBUG=False
SECRET_KEY=production-secret

DB_NAME=...
DB_USER=...
DB_PASSWORD=...
DB_HOST=...
DB_PORT=5432

CELERY_BROKER_URL=rediss://<user>:<password>@<host>:6379?ssl_cert_reqs=CERT_NONE
CELERY_RESULT_BACKEND=rediss://<user>:<password>@<host>:6379?ssl_cert_reqs=CERT_NONE
```

---

## 🔒 Security
- No secrets committed to GitHub
- Environment variables used for configuration
- DEBUG disabled in production

---

## ✅ Summary
This project demonstrates:
- Large-scale CSV imports
- Async background processing
- Clean Django architecture
- Real-world deployment trade-offs

