web: gunicorn product_importer.wsgi
worker: celery -A product_importer worker --pool=solo -l info
