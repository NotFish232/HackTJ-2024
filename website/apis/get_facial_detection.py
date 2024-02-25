import face_recognition
import cv2
import numpy as np
from PIL import Image
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

MAX_IMG_SIZE = 512


def get_facial_detection(
    image_path: str, target_image_path: str
) -> tuple[str, str] | None:
    image = face_recognition.load_image_file(image_path)

    target_image = face_recognition.load_image_file(target_image_path)
    target_face_encoding = face_recognition.face_encodings(target_image)

    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    for location, encoding in zip(face_locations, face_encodings):
        try:
            match = face_recognition.compare_faces(encoding, target_face_encoding)[0]
        except:
            continue

        if match:
            top, right, bottom, left = location

            recognition_path = f"{current_dir}/temp/box-{image_path.rsplit('/', 1)[1]}-{target_image_path.rsplit('/', 1)[1]}"
            cropped_path = f"{current_dir}/temp/crop-{image_path.rsplit('/', 1)[1]}-{target_image_path.rsplit('/', 1)[1]}"

            Image.fromarray(image[top:bottom, left:right]).save(cropped_path)
            cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 3)
            Image.fromarray(image).save(recognition_path)

            return recognition_path, cropped_path

    return None


def main() -> None:
    get_facial_detection("combined.png", "alan-2.png")


if __name__ == "__main__":
    main()
