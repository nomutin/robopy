"""ユニットテストで使い回すMonkeyPatch."""

from __future__ import annotations

import pytest
from dynamixel_sdk.port_handler import PortHandler
from dynamixel_sdk.protocol2_packet_handler import Protocol2PacketHandler
from dynamixel_sdk.robotis_def import COMM_RX_FAIL, COMM_SUCCESS


class PortHandlerMock(PortHandler):  # type: ignore[misc]
    """PortHandlerのテスト用ダミークラス."""

    def setBaudRate(self, baudrate: int) -> bool:  # noqa: N802
        """
        `setBaudRate`のモック.

        通信の部分を削除し, ボーレートの検証のみを行う.
        """
        return bool(self.getCFlagBaud(baudrate) > 0)


class Protocol2PacketHandlerMock(Protocol2PacketHandler):  # type: ignore[misc]
    """Protocol2PacketHandlerのテスト用ダミークラス."""

    def ping(  # noqa: PLR6301
        self,
        port: PortHandler,
        dxl_id: int,
    ) -> tuple[int, int, int]:
        """
        `ping`のモック.

        通信を行わず, ポートメイトとサーボIDからstatusを返す.
        """
        model_number = 0
        is_valid_port = port.port_name == "/dev/ttyUSB0"
        is_valid_servo_id = dxl_id in {11, 12, 13, 14, 15}
        if is_valid_port and is_valid_servo_id:
            return model_number, COMM_SUCCESS, 0
        return model_number, COMM_RX_FAIL, 0


@pytest.fixture()
def _mock_handlers(monkeypatch: pytest.MonkeyPatch) -> None:
    """PortHandlerとProtocol2PacketHandlerのモックを適用する."""
    monkeypatch.setattr(
        target="dynamixel_sdk.PortHandler",
        name=PortHandlerMock,
    )
    monkeypatch.setattr(
        target="dynamixel_sdk.Protocol2PacketHandler",
        name=Protocol2PacketHandlerMock,
    )
