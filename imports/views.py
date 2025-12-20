import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import ImportJob
from .tasks import import_products

@csrf_exempt
def upload(request):
    file = request.FILES["file"]

    upload_dir = os.path.join(settings.BASE_DIR, "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    path = os.path.join(upload_dir, file.name)

    with open(path, "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    job = ImportJob.objects.create(
        file_path=path,
        status="PENDING"
    )

    import_products.delay(job.id)

    return JsonResponse({"job_id": job.id})

def status(request, job_id):
    job = ImportJob.objects.get(id=job_id)
    return JsonResponse({
        "status": job.status,
        "processed": job.processed_rows,
        "total": job.total_rows,
        "error": job.error_message
    })
