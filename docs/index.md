# About Robopy

![python](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10-blue)
[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/rye/main/artwork/badge.json)](https://rye-up.com)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-blue)](http://mypy-lang.org/)
[![Lint and Test](https://github.com/nomutin/Robopy/actions/workflows/ci.yaml/badge.svg)](https://github.com/nomutin/Robopy/actions/workflows/ci.yaml)

Python だけでロボットを動かすためのAPIです.  
研究室の機器なら大体動かせるはずです.

* [OpenManipulatorX](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/overview/)
* [WidowX Robot Arm](https://www.unipos.net/find/product_item.php?id=3430)
* [Rakuda2](https://github.com/ROBOTIS-JAPAN-GIT/rakuda2_example)
* [Intel Realsense](https://www.intelrealsense.com/)

特殊な依存関係(ROS や librealsense)無しでロボットを動かしたりデータを取得したりできます.

```python
from robopy import RobotDriver, ControlTable, CameraDriver

leader = RobotDriver(port_name="/dev/ttyUSB0")
follower = RobotDriver(port_name="/dev/ttyUSB1")
camera = CameraDriver(camera_id=0)
actions, observations = [], []

for _ in range(100):
    leader_position = leader.read(ControlTable.PRESENT_POSITION)
    follower.write(ControlTable.GOAL_POSITION, leader_position)
    actions.append(leader_position)
    observations.append(camera.get_frame())
```
