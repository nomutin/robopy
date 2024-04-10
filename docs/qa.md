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

## RobotDriverのインスタンス作成に失敗する
