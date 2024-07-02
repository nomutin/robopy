# Q&A

## [`CameraDriver`][src.robopy.camera.CameraDriver] で使用する `camera_id` がわからない

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

## [`CameraDriver`][src.robopy.camera.CameraDriver] の映像が見たい

[Flask](https://flask.palletsprojects.com/en/3.0.x/) を使うと見やすいです.

```python
from collections.abc import Generator
import cv2
from flask import Flask, Response

CAMERA_INDEX = 0
MIMETYPE = "multipart/x-mixed-replace; boundary=frame"
FRAME_BOUNDARY = b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
app = Flask(__name__)

def video_frame_generator() -> Generator[bytes, None, None]:
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

!!! tip

    リモートサーバで実行する際には`80`のSSHトンネリングが必要です.
    ```sh
    ssh -L 8000:localhost:8000 server_name
    ```

## [`RobotDriver`][src.robopy.robot.RobotDriver] で使用する `port_name`・`servo_id`・`baudrate` がわからない

`port_name` は, Linux の場合は `ls /dev/ttyUSB*`, Mac の場合は`ls /dev/tty.*` で表示されるポート名を指定します.

`servo_id` と `baudrate` は, 各サーボに書き込まれている値の正しい組み合わせでないと通信できません.
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

for baudrate, servo_id in product(baudrates, servo_ids):
    if not port_handler.setBaudRate(baudrate):
        continue

    _, comm_result, dxl_error = packet_handler.ping(port_handler, servo_id)
    if comm_result == COMM_SUCCESS:
        print(f"[{baudrate=} {servo_id=}] ping succeeded.")

    port_handler.closePort()
```

## `RobotDriver` で取得できる値の一覧を知りたい

[rich](https://github.com/Textualize/rich) ライブラリを使って
[Dynamixel Wizard](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/)
みたいなことができます.

```python
from rich.live import Live
from rich.table import Table

from robopy import ControlTable, RobotDriver

port_name = "/dev/ttyUSB0"
servo_ids = [1, 2, 3, 4, 5]
baudrate = 1_000_000

robot = RobotDriver(
    port_name=port_name,
    baudrate=baudrate,
    servo_ids=servo_ids,
)


def generate_table() -> Table:
    table = Table(title=f"Control Table of {port_name}")
    table.add_column("Address", justify="right")
    table.add_column("Table Item", justify="left")
    table.add_column("Dtype", justify="right")
    table.add_column("Access", justify="left")

    for servo_id in servo_ids:
        table.add_column(f"#{servo_id}", justify="right")

    for control_table in ControlTable:
        if control_table.value.access == "R":
            style = "cyan"
        if control_table.value.access == "R/W(NVM)":
            style = "green"
        if control_table.value.access == "R/W":
            style = "magenta"

        table.add_row(
            str(control_table.value.address),
            control_table.name,
            control_table.value.dtype.name,
            control_table.value.access,
            *[str(i) for i in robot.read(control_table)],
            style=style,
        )
    return table


with Live(generate_table()) as live:
    while True:
        live.update(generate_table())
```
