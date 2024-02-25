import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vigilant.settings")

import django

django.setup()

from celery import Celery
from pathlib import Path
from apis.get_facial_detection import get_facial_detection
from apis.get_person_description import get_person_description
from apis.get_vehicles import get_vehicles
from apis.get_people import get_people
from apis.get_license_plate import get_license_plate
from web.models import (
    FacialDetectionResult,
    PersonDescriptionResult,
    VehicleIdentificationResult,
    PeopleGetAllResult,
    LicensePlateResult,
)

app = Celery("tasks", broker="redis://localhost//")

image_dir = Path(__file__).parent.parent / "apis/dataset"


def absolute_to_relative(path: str) -> str:
    return f"./{path[path.index('website'):]}"


@app.task
def run_facial_detection(
    initial_image: str = str(image_dir / "initial_image.png"),
) -> None:
    for file in image_dir.glob("facial-detection-*.png"):
        file = str(file)
        detection_result = get_facial_detection(file, initial_image)
        FacialDetectionResult(
            source_image=absolute_to_relative(file),
            target_image=absolute_to_relative(initial_image),
            found_match=detection_result is not None,
            box_result=(
                absolute_to_relative(detection_result[0]) if detection_result else None
            ),
            cropped_result=(
                absolute_to_relative(detection_result[1]) if detection_result else None
            ),
        ).save()


@app.task
def run_person_description(image: str = str(image_dir / "initial_image.png")) -> None:
    description = get_person_description(image)
    image = absolute_to_relative(image)
    PersonDescriptionResult(image=image, description=description).save()


@app.task
def run_vehicles(image: str = str(image_dir / "vehicles.png")) -> None:
    box_image, sub_cars = get_vehicles(image)
    image = absolute_to_relative(image)
    box_image = absolute_to_relative(box_image)

    for cropped_image, desc in sub_cars:
        cropped_image = absolute_to_relative(cropped_image)
        VehicleIdentificationResult(
            image=image,
            box_result=box_image,
            description=desc,
            cropped_result=cropped_image,
        ).save()


@app.task
def get_all_people(image: str = str(image_dir / "facial-detection-2.png")) -> None:
    box_image, sub_image_paths = get_people(image)
    image = absolute_to_relative(image)
    box_image = absolute_to_relative(box_image)
    for cropped_image in sub_image_paths:
        cropped_image = absolute_to_relative(cropped_image)
        PeopleGetAllResult(
            image=image, box_result=box_image, cropped_result=cropped_image
        ).save()


@app.task
def get_license_plate_str(image: str = str(image_dir / "license_plate.png")) -> None:
    license_plate = get_license_plate(image)
    image = absolute_to_relative(image)
    LicensePlateResult(image=image, license_plate=license_plate).save()


# run_facial_detection()
# run_person_description()
# run_vehicles()
# get_all_people()
# get_license_plate_str()
