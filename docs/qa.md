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
from dynamixel_sdk import COMM_SUCCESS, PortHandler, Protocol2PacketHandler

device_name = "/dev/ttyUSB1"
baudrates = [9600, 57600, 115200, 1000000, 2000000, 3000000, 4000000]
servo_ids = list(range(254))


for servo_id, baudrate in product(baudrates, servo_ids):
    port_handler = PortHandler(device_name)
    packet_handler = Protocol2PacketHandler()

    if not port_handler.openPort():
        continue

    if not port_handler.setBaudRate(baudrate):
        continue
        raise RuntimeError(msg)

    _, comm_result, dxl_error = packet_handler.ping(port_handler, servo_id)
    if comm_result == COMM_SUCCESS:
        print(f"[{baudrate=} {servo_id=}] ping succeeded.")

    port_handler.closePort()
```

## RobotDriverのインスタンス作成に失敗する
