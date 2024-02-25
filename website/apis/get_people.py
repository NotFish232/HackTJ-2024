from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image
import numpy as np
import base64
import webcolors
import io
import os


model = YOLO("yolov8n.pt")


MAX_IMG_SIZE = 512


current_dir = os.path.dirname(os.path.realpath(__file__))


def encode_image(image: Image.Image) -> str:
    width, height = image.size
    image = image.resize((min(width, MAX_IMG_SIZE), min(height, MAX_IMG_SIZE)))

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    data = buffer.getvalue()

    base64_image = base64.b64encode(data).decode("utf-8")
    return base64_image


def get_color_name(requested_color: tuple[int, int, int]) -> str:
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name

    return min_colors[min(min_colors.keys())]


def get_people(
    image_path: str,
) -> list[str]:
    image = np.array(Image.open(image_path))
    result = model.predict(image, device="cpu", verbose=False)[0]
    
    people_paths = []

    idx = 0
    for box in result.boxes:
        label = model.names[box.cls.item()]
        
        if label == "person":
            x1, y1, x2, y2 = [*map(int, box[0].xyxy[0])]
            cropped_image = image[y1:y2, x1:x2]
            path = f"{current_dir}/temp/{idx}-{image_path}"
            Image.fromarray(cropped_image).save(path)
            people_paths.append(path)

            idx += 1


    return people_paths


def main() -> None:
    print(get_people("people.png"))


if __name__ == "__main__":
    main()
