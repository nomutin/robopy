# Usage

## カメラ

Web カメラを使用するには, [`CameraDriver`][src.robopy.camera.CameraDriver] を使用します.
詳細は [API reference](api/camera.md) を参照してください. 

## ロボット

ロボットを制御するには, [`RobotDriver`][src.robopy.robot.RobotDriver] を使用します.
また、制御できる項目については [`ControlTable`][src.robopy.control_table.ControlTable] を参照してください.

## 例

### Leader-Follower

- 2つの RobotDriver を用いて同期処理で Leader-Fllower が実現できます.  
- トルクの ON/OFF には `RobotDriver.write` のアドレスに `ControlTable.TORQUE_ENABLE` を指定します.  
- 位置の制御には `RobotDriver.read/write` のアドレスに `ControlTable.GOAL_POSITION` を指定します.

```python
import time

import numpy as np

from robopy import CameraDriver, ControlTable, RobotDriver

# Constants
leader_port, follower_port = "/dev/ttyUSB0", "/dev/ttyUSB1"
baudrate = 1_000_000
servo_ids = [1, 2, 3, 4, 5]
camera_id = 4

# Initialize
leader = RobotDriver(leader_port, baudrate=baudrate, servo_ids=servo_ids)
follower = RobotDriver(follower_port, baudrate=baudrate, servo_ids=servo_ids)
camera_driver = CameraDriver(camera_id=camera_id)
input()

# Safety Check
leader.write(ControlTable.TORQUE_ENABLE, [1] * len(servo_ids))
follower.write(ControlTable.TORQUE_ENABLE, [1] * len(servo_ids))

leader_posisition = leader.read(ControlTable.PRESENT_POSITION)
follower_position = follower.read(ControlTable.PRESENT_POSITION)
delta = np.array(leader_posisition) - np.array(follower_position)
for i in range(30):
    current_position = follower_position + delta * i / 30
    follower.write(
        control_table=ControlTable.GOAL_POSITION,
        values=current_position.tolist(),
    )
    time.sleep(0.5)

leader.write(ControlTable.TORQUE_ENABLE, [0] * len(servo_ids))
input()

# Main Loop
while True:
    s = time.monotonic()
    current_position = leader.read(ControlTable.PRESENT_POSITION)
    follower.write(
        control_table=ControlTable.GOAL_POSITION,
        values=current_position,
    )
    frame = camera_driver.get_frame()
    print("FPS:", 1 / (time.monotonic() - s))
```
