# ruff: noqa: PLR2004
"""
Dynamixel のコントロールテーブル.

References
----------
- https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/
- https://www.besttechnology.co.jp/modules/knowledge

"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal

__all__ = [
    "ControlItem",
    "ControlTable",
    "Dtype",
    "OperatingMode",
    "cast_value",
]


class Dtype(Enum):
    """データ型."""

    UINT8 = auto()
    UINT16 = auto()
    UINT32 = auto()
    INT16 = auto()
    INT32 = auto()


@dataclass
class ControlItem:
    """
    `ControlTable`の各項目のデータ構造.

    Attributes
    ----------
    address : int
        メモリアドレス.
    num_bytes : Literal[1, 2, 4]
        占有するバイト数.
    dtype : Dtype
        データ型.
    access : Literal['R', 'R/W', 'R/W(NVM)']
        アクセス権限.
        `NVM`(不揮発メモリ)の書き換えを行う場合はトルクを切る必要がある.
    description : str
        項目の軽い説明.

    """

    address: int
    num_bytes: Literal[1, 2, 4]
    dtype: Dtype
    access: Literal["R", "R/W", "R/W(NVM)"]
    description: str


class ControlTable(Enum):
    """Dynamixelのコントロールテーブル."""

    MODEL_NUMBER = ControlItem(
        address=0,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R",
        description="Dynamixelのモデル番号",
    )
    MODEL_INFORMATION = ControlItem(
        address=2,
        num_bytes=4,
        dtype=Dtype.UINT32,
        access="R",
        description="Dynamixelのモデル情報",
    )
    VERSION_OF_FIRMWARE = ControlItem(
        address=6,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R",
        description="ファームウェアのバージョン",
    )
    ID = ControlItem(
        address=7,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W(NVM)",
        description="固有のID",
    )
    BAUDRATE = ControlItem(
        address=8,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W(NVM)",
        description="通信する際のボーレート, 0~7をとる",
    )
    RETURN_DELAY_TIME = ControlItem(
        address=9,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W(NVM)",
        description="応答遅延時間, 0でも問題ない",
    )
    DRIVE_MODE = ControlItem(
        address=10,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W(NVM)",
        description="回転方向などの設定",
    )
    OPERATING_MODE = ControlItem(
        address=11,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W(NVM)",
        description="動作モード",
    )
    SECONDARY_ID = ControlItem(
        address=12,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W(NVM)",
        description="識別のための2個目のID",
    )
    PROTOCOL_VERSION = ControlItem(
        address=13,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R",
        description="プロトコル",
    )
    HOMING_OFFSET = ControlItem(
        address=20,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R/W(NVM)",
        description="真の現在位置-PRESENT_POSITION",
    )
    MOVING_THRESHOLD = ControlItem(
        address=24,
        num_bytes=4,
        dtype=Dtype.UINT32,
        access="R/W(NVM)",
        description="移動中かどうかのしきい値",
    )
    TEMPERATURE_LIMIT = ControlItem(
        address=31,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W(NVM)",
        description="温度の上限値",
    )
    MAX_VOLTAGE_LIMIT = ControlItem(
        address=32,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W(NVM)",
        description="印加電圧の上限値",
    )
    MIN_VOLTAGE_LIMIT = ControlItem(
        address=34,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W(NVM)",
        description="印加電圧の下限値",
    )
    PWM_LIMIT = ControlItem(
        address=36,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W(NVM)",
        description="GOAL_PWMの絶対値の最大値",
    )
    CURRENT_LIMIT = ControlItem(
        address=38,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W(NVM)",
        description="GOAL_CURRENTの絶対値の最大値",
    )
    ACCELERATION_LIMIT = ControlItem(
        address=40,
        num_bytes=4,
        dtype=Dtype.UINT32,
        access="R/W(NVM)",
        description="PROFILE_ACCELERATIONの最大値",
    )
    VELOCITY_LIMIT = ControlItem(
        address=44,
        num_bytes=4,
        dtype=Dtype.UINT32,
        access="R/W(NVM)",
        description="GOAL_VELOCITYの絶対値の最大値",
    )
    MAX_POSITION_LIMIT = ControlItem(
        address=48,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R/W(NVM)",
        description="GOAL_POSITIONの最大値",
    )
    MIN_POSITION_LIMIT = ControlItem(
        address=52,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R/W(NVM)",
        description="GOAL_POSITIONの最小値",
    )
    SHUTDOWN = ControlItem(
        address=63,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W",
        description="シャットダウン状態, 0がON",
    )
    LED = ControlItem(
        address=65,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W",
        description="LEDのON/OFF, 0がOFF",
    )
    TORQUE_ENABLE = ControlItem(
        address=64,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R/W",
        description="トルクのON/OFF, 0がOFF",
    )
    HARDWARE_ERROR_STATUS = ControlItem(
        address=70,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R",
        description="ハードウェアエラーのステータス",
    )
    VELOCITY_I_GAIN = ControlItem(
        address=76,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W",
        description="速度制御のIゲイン",
    )
    VELOCITY_P_GAIN = ControlItem(
        address=78,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W",
        description="速度制御のPゲイン",
    )
    POSITION_D_GAIN = ControlItem(
        address=80,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W",
        description="位置制御のDゲイン",
    )
    POSITION_I_GAIN = ControlItem(
        address=82,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W",
        description="位置制御のIゲイン",
    )
    POSITION_P_GAIN = ControlItem(
        address=84,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R/W",
        description="位置制御のPゲイン",
    )
    GOAL_PWM = ControlItem(
        address=100,
        num_bytes=2,
        dtype=Dtype.INT16,
        access="R/W",
        description="PWM制御の目標値",
    )
    GOAL_CURRENT = ControlItem(
        address=102,
        num_bytes=2,
        dtype=Dtype.INT16,
        access="R/W",
        description="電流制御の目標値",
    )
    GOAL_VELOCITY = ControlItem(
        address=104,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R/W",
        description="速度制御の目標値",
    )
    PROFILE_ACCELERATION = ControlItem(
        address=108,
        num_bytes=4,
        dtype=Dtype.UINT32,
        access="R/W",
        description="Profileの加速度or加速時間",
    )
    PROFILE_VELOCITY = ControlItem(
        address=112,
        num_bytes=4,
        dtype=Dtype.UINT32,
        access="R/W",
        description="Profileの最大速度",
    )
    GOAL_POSITION = ControlItem(
        address=116,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R/W",
        description="位置制御の目標値",
    )
    REALTIME_TICK = ControlItem(
        address=120,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R",
        description="リアルタイムカウンタ(1ms周期)",
    )
    MOVING_STATUS = ControlItem(
        address=122,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R",
        description="動作中の状況",
    )
    PRESENT_PWM = ControlItem(
        address=124,
        num_bytes=2,
        dtype=Dtype.INT16,
        access="R",
        description="制御中のPWM出力値",
    )
    PRESENT_CURRENT = ControlItem(
        address=126,
        num_bytes=2,
        dtype=Dtype.INT16,
        access="R",
        description="サーボへ流れている電流値",
    )
    PRESENT_VELOCITY = ControlItem(
        address=128,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R",
        description="出力軸の回転数",
    )
    PRESENT_POSITION = ControlItem(
        address=132,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R",
        description="真の位置-Homing Offset",
    )
    VELOCITY_TRAJECTORY = ControlItem(
        address=136,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R",
        description="Profileによって生成された目標速度",
    )
    POSITION_TRAJECTORY = ControlItem(
        address=140,
        num_bytes=4,
        dtype=Dtype.INT32,
        access="R",
        description="Profileによって生成された目標位置",
    )
    PRESENT_INPUT_VOLTAGE = ControlItem(
        address=144,
        num_bytes=2,
        dtype=Dtype.UINT16,
        access="R",
        description="印加電圧",
    )
    PRESENT_TEMPERATURE = ControlItem(
        address=146,
        num_bytes=1,
        dtype=Dtype.UINT8,
        access="R",
        description="内部温度",
    )

    def __init__(self, control_item: ControlItem) -> None:
        """
        コントロールテーブルの各項目のデータ構造を設定する.

        これが無いと `ControlTable.BAUDRATE.address` みたいなアクセスができない
        """
        self.address = control_item.address
        self.num_bytes = control_item.num_bytes
        self.dtype = control_item.dtype
        self.access = control_item.access
        self.description = control_item.description


class OperatingMode(Enum):
    """
    動作モード.

    Attributes
    ----------
    CURRENT_CONTROL_MODE : int
        電流制御. 位置及び速度制御は行わない.
    VELOCITY_CONTROL_MODE : int
        速度制御. 位置及びトルク制御は行わない.
    POSITION_CONTROL_MODE : int
        位置制御.
    EXTENDED_POSITION_CONTROL_MODE : int
        位置制御. GoalPositionの範囲が拡大.
    CURRENT_BASE_POSITION_CONTROL_MODE : int
        電流制限付き位置制御.
    PWM_CONTROL_MODE : int
        PWMのデューティー比で制御.

    """

    CURRENT_CONTROL_MODE = 0
    VELOCITY_CONTROL_MODE = 1
    POSITION_CONTROL_MODE = 3
    EXTENDED_POSITION_CONTROL_MODE = 4
    CURRENT_BASE_POSITION_CONTROL_MODE = 5
    PWM_CONTROL_MODE = 16


def cast_value(value: float, dtype: Dtype) -> int:
    """
    値を各データ型に合わせた値にする.

    PRESENT_POSITIONやPRESENT_CURRENTは値の範囲を超えた値を
    取得してきてしまう場合があるらしい.

    Examples
    --------
    >>> value = 2 ** 15 + 1
    >>> cast_value(value, ControlTable.PRESENT_CURRENT.dtype)
    >>> -32767

    """
    if dtype == Dtype.UINT8:
        value = int(value) & 0xFF
    if dtype == Dtype.UINT16:
        value = int(value) & 0xFFFF
    if dtype == Dtype.UINT32:
        value = int(value) & 0xFFFFFFFF
    if dtype == Dtype.INT16:
        value = int(value) & 0xFFFF
        if value >= 0x8000:
            value -= 0x10000
    if dtype == Dtype.INT32:
        value = int(value) & 0xFFFFFFFF
        if value >= 0x80000000:
            value -= 0x100000000
    return int(value)
