from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from PIL import Image
import numpy as np
import base64
import webcolors
import io
import os


current_dir = os.path.dirname(os.path.realpath(__file__))


model = YOLO(f"{current_dir}/yolov8n.pt")
VEHICLE_LABELS = (
    "car",
    "bicyle",
    "motorcyle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
)


MAX_IMG_SIZE = 512


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


def get_vehicles(
    image_path: str,
) -> tuple[str, list[tuple[str, str]]]:
    image = np.array(Image.open(image_path))
    result = model.predict(image, device="cpu", verbose=False)[0]
    annotator = Annotator(image, font_size=1, line_width=1)
    vehicle_data = []

    idx = 0
    for box in result.boxes:
        label = model.names[box.cls.item()]
        if label in VEHICLE_LABELS:
            idx += 1
            x1, y1, x2, y2 = [*map(int, box[0].xyxy[0])]
            cropped_image = image[y1:y2, x1:x2]
            cropped_url = f"{current_dir}/temp/{idx}-{image_path.rsplit('/', 1)[1]}"
            Image.fromarray(cropped_image).save(cropped_url)
            color = get_color_name(np.mean(cropped_image, axis=(0, 1)).astype(np.int32))
            description = f"{color} {label}"
            annotator.box_label(box.xyxy[0], description, color=(255, 0, 0))

            vehicle_data.append((cropped_url, description))

    out_path = f"{current_dir}/temp/{image_path.rsplit('/', 1)[1]}"
    Image.fromarray(image).save(out_path)

    return out_path, vehicle_data


def main() -> None:
    print(get_vehicles("cars.png"))


if __name__ == "__main__":
    main()
