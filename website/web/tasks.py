import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vigilant.settings")

import django

django.setup()

from celery import Celery
from pathlib import Path
from apis.get_facial_detection import get_facial_detection
from web.models import FacialDetectionResult

app = Celery("tasks", broker="redis://localhost//")

image_dir = Path(__file__).parent.parent / "apis/dataset"


@app.task
def run_facial_detection() -> None:
    initial_image = str(image_dir / "initial_image.png")
    for file in image_dir.glob("facial-detection-*.png"):
        file = str(file)
        detection_result = get_facial_detection(file, initial_image)
        FacialDetectionResult(
            source_image=file,
            target_image=initial_image,
            found_match=detection_result is not None,
            box_result=detection_result[0] if detection_result else None,
            cropped_result=detection_result[1] if detection_result else None,
        ).save()
