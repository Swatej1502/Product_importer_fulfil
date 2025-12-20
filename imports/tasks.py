import csv
from celery import shared_task
from django.db import connection
from .models import ImportJob

@shared_task
def import_products(job_id):
    job = ImportJob.objects.get(id=job_id)
    job.status = "IMPORTING"
    job.save()

    try:
        with open(job.file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            job.total_rows = len(rows)
            job.save()

            batch = []
            for index, row in enumerate(rows, start=1):
                batch.append((
                    row["sku"],
                    row["name"],
                    row.get("description", ""),
                    True
                ))

                if len(batch) == 1000:
                    save_batch(batch)
                    batch.clear()

                job.processed_rows = index
                job.save(update_fields=["processed_rows"])

            if batch:
                save_batch(batch)

        job.status = "COMPLETED"
        job.save()

    except Exception as e:
        job.status = "FAILED"
        job.error_message = str(e)
        job.save()

def save_batch(batch):
    with connection.cursor() as cursor:
        cursor.executemany("""
            INSERT INTO products_product (sku, name, description, active)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (LOWER(sku))
            DO UPDATE SET
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                active = EXCLUDED.active
        """, batch)
