# Q&A

## `CameraDriver` で使用する `camera_id` がわからない

まず、USBポートにカメラが接続されているかを確認してください.  
その後、[opencv-python](https://pypi.org/project/opencv-python/) を使って総当たりでカメラを探すことができます.

```python
import cv2

available_cameras = []

for camera_id in range(20):
    capture = cv2.VideoCapture(camera_id, cv2.CAP_ANY)
    if not capture.isOpened() or not capture.read()[0]:
        continue
    available_cameras.append(camera_id)
    capture.release()

print(f"Available cameras: {available_cameras}")
```

## `CameraDriver` の映像が見たい

[Flask](https://flask.palletsprojects.com/en/3.0.x/) を使うと見やすいです.

```python
from collections.abc import Iterator
import cv2
from flask import Flask, Response

CAMERA_INDEX = 0
MIMETYPE = "multipart/x-mixed-replace; boundary=frame"
FRAME_BOUNDARY = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
app = Flask(__name__)

def video_frame_generator() -> Iterator[bytes]:
    cap = cv2.VideoCapture(CAMERA_INDEX)
    while True:
        success, frame = cap.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield b"".join([FRAME_BOUNDARY, frame_bytes, b"\r\n"])

@app.route("/")
def stream_video() -> Response:
    return Response(video_frame_generator(), mimetype=MIMETYPE)

if __name__ == "__main__":
    app.run(host="localhost", port=8000)
```

リモートサーバで実行する際には`80`のSSHトンネリングが必要です.

```sh
ssh -L 8000:localhost:8000
```

## `RobotDriver` で使用する `port_name` がわからない

Linux の場合は `ls /dev/ttyUSB*`, Mac の場合は`ls /dev/tty.*` で表示されるファイル名が `port_name` になります.

## `RobotDriver` で使用する `servo_id`・`baudrate` がわからない

`RobotDriver` をインスタンス化するには, 各サーボに書き込まれている ID と ボーレート の正しい組み合わせが必要になります.
総当たりで調べましょう.

```python
from itertools import product
from dynamixel_sdk import COMM_SUCCESS, PortHandler, Protocol2PacketHandler

device_name = "/dev/ttyUSB1"
baudrates = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000]
servo_ids = list(range(254))

port_handler = PortHandler(device_name)
packet_handler = Protocol2PacketHandler()

if not port_handler.openPort():
    raise RuntimeError("Failed to open port.")

for servo_id, baudrate in product(baudrates, servo_ids):
    if not port_handler.setBaudRate(baudrate):
        continue

    _, comm_result, dxl_error = packet_handler.ping(port_handler, servo_id)
    if comm_result == COMM_SUCCESS:
        print(f"[{baudrate=} {servo_id=}] ping succeeded.")

    port_handler.closePort()
```
