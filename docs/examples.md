# Examples

## Dynamixel Wizard

```python
from rich.live import Live
from rich.table import Table

from robopy import ControlTable, RobotDriver

robot = RobotDriver(
    port_name="/dev/ttyUSB0",
    baudrate=[11, 12, 13, 14, 15],
    servo_ids=1_000_000,
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

## Leader-Follower

```python
from __future__ import annotations

import threading
import time
from pathlib import Path

import numpy as np

from robopy import CameraDriver, ControlTable, OperatingMode, RobotDriver


class KeyBoardInputThread(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.key_pushed = False
        self._stop_event = threading.Event()

    def run(self) -> None:
        while not self._stop_event.is_set():
            input()
            self.key_pushed = not self.key_pushed

    def stop(self) -> None:
        self._stop_event.set()


def main() -> None:
    save_dir, seq_len = Path("data"), 200
    leader = RobotDriver(
        port_name="/dev/ttyUSB0",
        baudrate=1_000_000,
        servo_ids=[1, 2, 3, 4, 5],
    )
    follower = RobotDriver(
        port_name="/dev/ttyUSB1",
        baudrate=1_000_000,
        servo_ids=[1, 2, 3, 4, 5],
    )

    leader.write(ControlTable.TORQUE_ENABLE, [0] * 5)
    follower.write(ControlTable.TORQUE_ENABLE, [1] * 5)

    camera_driver = CameraDriver(camera_id=4)
    rich_logger = RichLogger(title="Leader-Follower Status")
    rich_logger.start()
    key_event = KeyBoardInputThread()
    key_event.start()

    act_list = []
    obs_list = []

    data_idx = len(list(save_dir.glob("action_*.npy")))

    try:
        while True:
            s = time.monotonic()
            current_position = leader.read(ControlTable.PRESENT_POSITION)
            follower.write(
                control_table=ControlTable.GOAL_POSITION,
                values=current_position,
            )
            frame = camera_driver.get_frame()

            if key_event.key_pushed:
                act_list.append(frame)
                obs_list.append(current_position)
            else:
                act_list.clear()
                obs_list.clear()

            if len(act_list) == seq_len:
                act_path = save_dir / f"action_{data_idx}.npy"
                obs_path = save_dir / f"observation_{data_idx}.npy"
                np.save(act_path, np.stack(act_list, axis=0))
                np.save(obs_path, np.stack(obs_list, axis=0))
                data_idx += 1
                key_event.key_pushed = False

            print("FPS:", 1 / (time.monotonic() - s))
            print("Length:", len(act_list))
    finally:
        key_event.stop()
        key_event.join()


if __name__ == "__main__":
    main()
```
