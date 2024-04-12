# About robopy 🤖🐍

![python](https://img.shields.io/badge/python-3.7%20|%203.8%20|%203.9%20|%203.10-blue)

Python だけでロボットを動かすためのAPIです.  
研究室の機器なら大体動かせるはずです.

* [OpenManipulatorX](https://emanual.robotis.com/docs/en/platform/openmanipulator_x/overview/)
* [WidowX Robot Arm](https://www.unipos.net/find/product_item.php?id=3430)
* [Rakuda2](https://github.com/ROBOTIS-JAPAN-GIT/rakuda2_example)
* [Intel Realsense](https://www.intelrealsense.com/)

特殊な依存関係(ROS や librealsense)無しでロボットを動かしたりデータを取得したりできます.

```sh
pip install git+https://github.com/nomutin/robopy.git
```

```python
from robopy import RobotDriver, ControlTable, CameraDriver

leader = RobotDriver(port_name="/dev/ttyUSB0")
follower = RobotDriver(port_name="/dev/ttyUSB1")
camera = CameraDriver(camera_id=0)
action_list, observation_list = [], []

for _ in range(100):
    leader_position = leader.read(ControlTable.PRESENT_POSITION)
    follower.write(ControlTable.GOAL_POSITION, leader_position)
    action_list.append(leader_position)
    observation_list.append(camera.get_frame())
```
