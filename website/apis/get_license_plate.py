from PIL import Image
import subprocess


def get_license_plate(image_path: str) -> str:
    try:
        result = subprocess.run(
            ["alpr", image_path, "-n", "1"], capture_output=True, text=True
        )
        license_plate = result.stdout.split("-", 1)[1].split("\t", 1)[0].strip()
        return license_plate
    except:
        return ""


def main() -> None:
    print(get_license_plate("car.jpg"))


if __name__ == "__main__":
    main()
