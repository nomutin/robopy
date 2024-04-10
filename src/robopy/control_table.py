# ruff: noqa: PLR2004
"""
Dynamixel のコントロールテーブル関連.

References
----------
- [ROBOTIS E-manual](https://emanual.robotis.com/docs/en/dxl/x/xm430-w350/)
- [X Series Control table](https://www.besttechnology.co.jp/modules/knowledge/?X%20Series%20Control%20table)

"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Literal


class Dtype(Enum):
    """
    `ControlItem`のデータ型.

    Attributes
    ----------
    UINT8 : int
        8bit符号なし整数.
    UINT16 : int
        16bit符号なし整数.
    UINT32 : int
        32bit符号なし整数.
    INT16 : int
        16bit符号あり整数.

    """

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
    """
    Dynamixelのコントロールテーブル.

    References
    ----------
    - [X Series Control table](https://www.besttechnology.co.jp/modules/knowledge/?X%20Series%20Control%20table)

    Attributes
    ----------
    MODEL_NUMBER : ControlItem
        Dynamixel のモデル番号.
        モデル固有の値を保持する.
        異なる種類の Dynamixel を混在して使用する際の個体識別などに使用できる.
    MODEL_INFORMATION : ControlItem
        Dynamixelのモデル情報.
        異なる種類の Dynamixel を混在して使用する際の個体識別などに使用できる.
    VERSION_OF_FIRMWARE : ControlItem
        内蔵される CPU に書き込まれたプログラムのバージョン.
        ファームウェアの更新を行った際に合わせて自動的に変更される.
    ID : ControlItem
        各 Dynamixel を特定するための固有の値で0~252の範囲の数値で設定する.
        同一ネットワーク内に存在する Dynamixel には各々異なるIDが要求される.
    BAUDRATE : ControlItem
        通信する際のボーレート.
        ホストとDynamixelのボーレートは一致させる必要がある.
        詳しくは `::: Baudrate` を参照.
    RETURN_DELAY_TIME : ControlItem
        インストラクションパケットが送られた後、ステータスパケットを返すまでの待ち時間.
        0を設定しても問題ない.

        `Delay Time [us] = Value * 2 [us]`
    DRIVE_MODE : ControlItem
        デフォルト回転方向・デュアルジョイント・プロファイル構成を設定する.
        デフォルト回転方向によりはPosition・Velocity・PWMの各指令によるホーンの回転方向が変化する.

        - `0`: Direction of rotation (0:Normal, 1:Reverse)
        - `1`: Profile configuration (0:Master, 1:Slaver, X540シリーズのみ)
        - `2`: Dual Joint (0:Velocity-based Profile, 1:Time-based Profile)
    OPERATING_MODE : ControlItem
        動作モード. 詳しくは `::: OperatingMode` を参照.
    SECONDARY_ID : ControlItem
        DynamixelのSecondary ID.
        Secondary ID は、ID と同様に各 Dynamixel を識別するために用いられる.
        なお、Secondary IDに253以上の値が設定されている場合機能しない。
    PROTOCOL_VERSION : ControlItem
        通信プロトコルのバージョン.
        異なるプロトコルを混在させて使用する事はできない.
        基本的には1か2を選択する.
    HOMING_OFFSET : ControlItem
        この値が真の現在位置に加算され `PRESENT_POSITION` に反映される.
        オフセット位置をホスト側では無く Dynamixel 側に持たせる際に使用する.
        真の現在位置とは, Multi Turn が off・Homing Offset が 0・
        Direction of rotation が0の時の`PRESENT_POSITION` を意味する.

        `Position [deg] = Value * 360 [deg] / 4095`
    MOVING_THRESHOLD : ControlItem
        `PRESENT_VELOCITY` の絶対値と比較した結果が `MOVING` に示される.

        `Velocity [rpm] = Value * 0.229 [rpm]`
    TEMPERATURE_LIMIT : ControlItem
        `PRESENT_TEMPERATURE` がこの値を超えると
        `HARDWARE_ERROR_STATUS` の該当ビットがONになり,
        `SHUTDOWN` で指定された動作に遷移する.
    MAX_VOLTAGE_LIMIT : ControlItem
        `PRESENT_INPUT_VOLTAGE` がこの値を超えると
        `HARDWARE_ERROR_STATUS` の該当ビットがONになり,
        `SHUTDOWN` で指定された動作に遷移する.

        `Voltage [V] = Value * 0.1 [V]`
    MIN_VOLTAGE_LIMIT : ControlItem
        `PRESENT_INPUT_VOLTAGE` がこの値を下回ると
        `HARDWARE_ERROR_STATUS` の該当ビットがONになり,
        `SHUTDOWN` で指定された動作に遷移する。
    PWM_LIMIT : ControlItem
        `GOAL_PWM` の絶対値はこの値以下に制限される.

        `Duty [%] = Value * 100 [%] / 855`
    CURRENT_LIMIT : ControlItem
        `GOAL_CURRENT` の絶対値はこの値以下に制限される.

        `Current [mA] = Value * CurrentScalingFactor [mA]`
    ACCELERATION_LIMIT : ControlItem
        `PROFILE_ACCELERATION` の絶対値はこの値以下に制限される.

        `Acceleration [rpm²] = Value * 214.577`
    VELOCITY_LIMIT : ControlItem
        `GOAL_VELOCITY` の絶対値と `PROFILE_VELOCITY` はこの値以下に制限される.

        `Velocity [rpm] = Value * 0.229 [rpm]`
    MAX_POSITION_LIMIT : ControlItem
        `OPERATING_MODE` に `POSITION_CONTROL_MODE`が設定されている時に
        `GOAL_POSITION` はこの値の範囲内に制限される.

        `Position [deg] = Value * 360 [deg] / 4096`
    MIN_POSITION_LIMIT : ControlItem
        `OPERATING_MODE` に `POSITION_CONTROL_MODE`が設定されている時に
        `GOAL_POSITION` はこの値の範囲内に制限される.
    SHUTDOWN : ControlItem
        この設定と `HARDWARE_ERROR_STATUS` の論理積が0以外になると,
        `TORQUE_ENABLE` は0になりモータの出力が遮断さる.
        以後 `TORQUE_ENABLE` を1にする事はできない.

        - `0`: Input Voltage Error
        - `2`: Overheating Error
        - `3`: Motor Encoder Error
        - `4`: Electrical Shock Error
        - `5`: Overload Error

        なお、シャットダウン状態から復帰するには発生している障害を排除した後、
        電源の再投入か、REBOOTインストラクションパケットを受信する必要がある.
    TORQUE_ENABLE : ControlItem
        出力軸をフリーにするか `OPERATION_MODE` に従った制御を開始する。

        - `0`: 出力軸フリー・制御停止・ロックされたアイテムを解除
        - `1`: `OPERATION_MODE`に従った制御開始、NVMのアイテムロック
    LED : ControlItem
        本体に装備されたLEDを点灯ないし消灯する.

        - `0`: 消灯
        - `1`: 点灯
    HARDWARE_ERROR_STATUS : ControlItem
        様々なフィードバックと内部の制御状態を比較した結果を示す.
        `SHUTDOWN`と同じ出力.
    VELOCITY_I_GAIN : ControlItem
        速度制御演算におけるIゲインを指定する。
        `OPERATION_MODE` に `VELOCITY_CONTROL_MODE` が設定されている時に有効.

        `KvI = (Velocity I Gain) / 65536`
    VELOCITY_P_GAIN : ControlItem
        速度制御演算におけるPゲインを指定する。
        `OPERATION_MODE` に `VELOCITY_CONTROL_MODE` が設定されている時に有効.

        `KvP = (Velocity P Gain) / 128`

    """

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


class Baudrate(Enum):
    """
    通信する際のボーレート.

    Notes
    -----
    - デフォルトでは `Baudrate.BPS_1M` が設定されているはず.
    - ホストのボーレートはBPS値を直接指定するので注意.
    - ホストとボーレートが合わないと通信できないので注意.

    Attributes
    ----------
    BPS_9600 : int
        9600bps.
    BPS_57600 : int
        57600bps.
    BPS_115200 : int
        115200bps.
    BPS_1M : int
        1Mbps.
    BPS_2M : int
        2Mbps.
    BPS_3M : int
        3Mbps.
    BPS_4M : int
        4Mbps.

    """

    BPS_9600 = 1
    BPS_57600 = 2
    BPS_115200 = 3
    BPS_1M = 4
    BPS_2M = 5
    BPS_3M = 6
    BPS_4M = 7


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
