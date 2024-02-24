import requests 
import shutil

base_url =  "https://itsvideo.arlingtonva.us:8013/live/cam214.stream"
url = f"{base_url}/playlist.m3u8"



x = requests.get(url).text.split("\n")[-2]
print(x)
y = []
for line in requests.get(f"{base_url}/{x}").text.split("\n"):
    if line.endswith("ts"):
        y.append(line)
print(requests.get(f"{base_url}/{x}").text)
for j in y:
    with requests.get(f"{base_url}/{j}", stream=True) as r:
        with open(j, 'wb') as f:
            shutil.copyfileobj(r.raw, f)