# Q&A

## CameraDriver で使用する camera_id がわからない

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

このようなコードを実行して、利用可能なカメラのIDを調べてください.

## `RobotDriver` で使用する port がわからない

## RobotDriver で使用する servo_id がわからない

```python
"""サーボの`motor_id`を特定するためのスクリプト."""

from dynamixel_sdk import COMM_SUCCESS, PortHandler, Protocol2PacketHandler
from tqdm import tqdm

device_name = "/dev/ttyUSB1"
baudrates = [
    9600,
    19200,
    38400,
    57600,
    115200,
    230400,
    460800,
    500000,
    576000,
    921600,
    1000000,
    1152000,
    2000000,
    2500000,
    3000000,
    3500000,
    4000000,
]

for baudrate in baudrates:
    port_handler = PortHandler(device_name)
    packet_handler = Protocol2PacketHandler()

    if not port_handler.openPort():
        msg = f"Failed to open port {device_name}"
        raise RuntimeError(msg)

    if not port_handler.setBaudRate(baudrate):
        msg = f"Failed to set baudrate to {baudrate}"
        raise RuntimeError(msg)

    for dxl_id in tqdm(range(254)):
        _, comm_result, dxl_error = packet_handler.ping(port_handler, dxl_id)
        if comm_result == COMM_SUCCESS:
            print(f"[{baudrate=} {dxl_id=}] ping succeeded.")

    port_handler.closePort()
```

## RobotDriverのインスタンス作成に失敗する
