"""
Dynamixelを組み合わせたロボットを制御するクラス.

研究室のロボットには大体使えます
- OpenManipulator-X
- WidowX
- Rakuda-2
"""

from __future__ import annotations

import dynamixel_sdk

from robopy.control_table import ControlTable
from robopy.dynamixel import DynamixelDriver

__all__ = ["RobotDriver"]


class RobotDriver:
    """ロボット全体のクラス."""

    def __init__(
        self,
        port_name: str,
        baudrate: int,
        servo_ids: list[int],
    ) -> None:
        """
        接続と各サーボのI/Oの確立.

        Parameters
        ----------
        port_name : str
            シリアルポートの名前.
            `ls /dev` で確認できる.
        baudrate : int
            ボーレート. サーボに設定された値と揃える必要がある.
        servo_id : int
            サーボのID. packetHandlerの通信の確認に使用する.

        Raises
        ------
        RuntimeError
            - ポートのオープンに失敗した場合
            - ボーレートの設定に失敗した場合
            - 全サーボのpingに失敗した場合

        """
        self.port_handler = dynamixel_sdk.PortHandler(port_name=port_name)
        self.packet_handler = dynamixel_sdk.Protocol2PacketHandler()

        if not self.port_handler.openPort():
            msg = f"Failed to open port {port_name}"
            raise RuntimeError(msg)

        if not self.port_handler.setBaudRate(baudrate):
            msg = f"Failed to set baudrate to {baudrate}"
            raise RuntimeError(msg)

        for servo_id in servo_ids:
            _, comm_result, _ = self.packet_handler.ping(
                port=self.port_handler,
                dxl_id=servo_id,
            )
            if comm_result != dynamixel_sdk.COMM_SUCCESS:
                msg = f"Failed to ping servo {servo_id}"
                raise RuntimeError(msg)

        self.servos = [
            DynamixelDriver(
                port_handler=self.port_handler,
                packet_handler=self.packet_handler,
                servo_id=servo_id,
            )
            for servo_id in servo_ids
        ]

    def write(self, control_table: ControlTable, values: list[int]) -> None:
        """各サーボに値を書き込む."""
        for servo, value in zip(self.servos, values):
            servo.write(control_table, value)

    def read(self, control_table: ControlTable) -> list[int]:
        """各サーボから値を読み取る."""
        return [servo.read(control_table) for servo in self.servos]
