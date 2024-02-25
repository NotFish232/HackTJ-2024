import requests
import shutil
import os
import cv2

FPS = 15
IMG_SIZE = 512

current_dir = os.path.dirname(os.path.realpath(__file__))
with open(f"{current_dir}/available_camera_feeds.txt", "r") as f:
    AVAILABLE_CAMERA_FEEDS = f.read().split("\n")


def get_live_feed(base_url: str) -> str:
    try:
        initial_url = f"{base_url}/playlist.m3u8"

        r = requests.get(initial_url)
        chunk_url = next(l for l in r.text.split("\n") if l.endswith(".m3u8"))

        r = requests.get(f"{base_url}/{chunk_url}")
        ts_urls = [l for l in r.text.split("\n") if l.endswith(".ts")]

        out_url = f"{current_dir}/temp/{base_url.rsplit('/', -1)[-1].split('.', 1)[0]}.mp4"
        writer = cv2.VideoWriter(
            out_url, cv2.VideoWriter_fourcc(*"mp4v"), FPS, (IMG_SIZE, IMG_SIZE)
        )

        for ts_url in ts_urls:
            with requests.get(f"{base_url}/{ts_url}", stream=True) as r:
                with open(f"{current_dir}/temp/{ts_url}", "wb") as f:
                    shutil.copyfileobj(r.raw, f)

            path = f"{current_dir}/temp/{ts_url}"
            cap = cv2.VideoCapture(path)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
                writer.write(frame)

            cap.release()

            os.remove(path)

        writer.release()

        return out_url
    except:
        return ""


def main() -> None:
    print(get_live_feed(AVAILABLE_CAMERA_FEEDS[100]))


if __name__ == "__main__":
    main()
