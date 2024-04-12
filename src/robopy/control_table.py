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

    """

    address: int
    num_bytes: Literal[1, 2, 4]
    dtype: Dtype
    access: Literal["R", "R/W", "R/W(NVM)"]


class ControlTable(Enum):
    """
    Dynamixelのコントロールテーブル.

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
        本体に装備されたLEDを点灯/消灯する.

        - `0`: 消灯
        - `1`: 点灯
    HARDWARE_ERROR_STATUS : ControlItem
        様々なフィードバックと内部の制御状態を比較した結果を示す.
        `SHUTDOWN`と同じ出力.
    VELOCITY_I_GAIN : ControlItem
        速度制御演算におけるIゲイン.
        `OPERATION_MODE` に `VELOCITY_CONTROL_MODE` が設定されている時に有効.

        `KvI = (Velocity I Gain) / 65536`
    VELOCITY_P_GAIN : ControlItem
        速度制御演算におけるPゲイン.
        `OPERATION_MODE` に `VELOCITY_CONTROL_MODE` が設定されている時に有効.

        `KvP = (Velocity P Gain) / 128`
    POSITION_D_GAIN : ControlItem
        位置制御演算におけるDゲイン.
        `OPERATION_MODE` に `*POTION_CONTROL_MODE` が設定されているときに有効.

        `KpD = (Position I Gain) / 16`
    POSITION_I_GAIN : ControlItem
        位置制御演算におけるIゲイン.
        `OPERATION_MODE` に `POSITION_CONTROL_MODE` が設定されている時に有効.

        `KpI = (Position I Gain) / 65536`
    POSITION_P_GAIN : ControlItem
        位置制御演算におけるPゲイン.
        `OPERATION_MODE` に `POSITION_CONTROL_MODE` が設定されている時に有効.

        `KpP = (Position P Gain) / 128`
    FEEDFORWARD_ACCELERATION_GAIN : ControlItem
        位置制御演算における加速度フィードフォワードゲイン.
        OPERATION_MODE` に `POSITION_CONTROL_MODE` が設定されている時に有効.
    FEEDFORWARD_VELOCITY_GAIN : ControlItem
        位置制御演算における速度フィードフォワードゲイン.
        `OPERATION_MODE` に `POSITION_CONTROL_MODE` が設定されている時に有効.
    GOAL_PWM : ControlItem
        PWMのデューティー比.
        全ての `OPERATION_MODE`において、
        制御の最終段にこの値以下にデューティー比が制限されモータへ印加される.

        `Duty [%] = Value * 100 [%] / 855`
    GOAL_CURRENT : ControlItem
        電流制御演算における目標電流を指定する。
        `OPERATION_MODE` に `CURRENT_*_MODE` が設定されている時に有効.

        `Current [mA] = Value * ScalingFactor [mA]`
    GOAL_VELOCITY : ControlItem
        速度制御の目標値.
        `OPERATION_MODE` に `VELOCITY_CONTROL_MODE` が設定されている時に有効.

        `Velocity [rpm] = Value * 0.229 [rpm]`
    PROFILE_ACCELERATION : ControlItem
        Profileの加速度もしくは加速時間.
        `OPERATION_MODE` が `CURRENT_CONTROL_MODE` 以外のときに有効.

        `Acceleration [rpm²] = Value * 214.577`
    PROFILE_VELOCITY : ControlItem
        Profileの速度.
        Drive ModeのProfile Configurationが0の時にProfileの最大速度を指定する.
        `CURRENT_CONTROL_MODE` / `VELOCITY_CONTROL_MODE` 以外のとき有効.
    GOAL_POSITION : ControlItem
        位置制御の目標値.
        `OPERATING_MODE` が `*_POSITION_CONTROL_MODE` のとき有効.
        各Mode毎に指摘できる数値範囲が異なる.
    REALTIME_TICK : ControlItem
        15ビットのフリーランカウンタ. 1ms周期毎にインクリメントされる.

    """

    MODEL_NUMBER = ControlItem(0, 2, Dtype.UINT16, "R")
    MODEL_INFORMATION = ControlItem(2, 4, Dtype.UINT32, "R")
    VERSION_OF_FIRMWARE = ControlItem(6, 1, Dtype.UINT8, "R")
    ID = ControlItem(7, 1, Dtype.UINT8, "R/W(NVM)")
    BAUDRATE = ControlItem(8, 1, Dtype.UINT8, "R/W(NVM)")
    RETURN_DELAY_TIME = ControlItem(9, 1, Dtype.UINT8, "R/W(NVM)")
    DRIVE_MODE = ControlItem(10, 1, Dtype.UINT8, "R/W(NVM)")
    OPERATING_MODE = ControlItem(11, 2, Dtype.UINT16, "R/W(NVM)")
    SECONDARY_ID = ControlItem(12, 1, Dtype.UINT8, "R/W(NVM)")
    PROTOCOL_VERSION = ControlItem(13, 1, Dtype.UINT8, "R")
    HOMING_OFFSET = ControlItem(20, 4, Dtype.INT32, "R/W(NVM)")
    MOVING_THRESHOLD = ControlItem(24, 4, Dtype.UINT32, "R/W(NVM)")
    TEMPERATURE_LIMIT = ControlItem(31, 1, Dtype.UINT8, "R/W(NVM)")
    MAX_VOLTAGE_LIMIT = ControlItem(32, 2, Dtype.UINT16, "R/W(NVM)")
    MIN_VOLTAGE_LIMIT = ControlItem(34, 2, Dtype.UINT16, "R/W(NVM)")
    CURRENT_LIMIT = ControlItem(38, 2, Dtype.UINT16, "R/W(NVM)")
    PWM_LIMIT = ControlItem(40, 2, Dtype.UINT16, "R/W(NVM)")
    ACCELERATION_LIMIT = ControlItem(44, 4, Dtype.UINT32, "R/W(NVM)")
    VELOCITY_LIMIT = ControlItem(48, 4, Dtype.UINT32, "R/W(NVM)")
    MAX_POSITION_LIMIT = ControlItem(52, 4, Dtype.INT32, "R/W(NVM)")
    MIN_POSITION_LIMIT = ControlItem(56, 4, Dtype.INT32, "R/W(NVM)")
    SHUTDOWN = ControlItem(63, 1, Dtype.UINT8, "R/W")
    LED = ControlItem(65, 1, Dtype.UINT8, "R/W")
    TORQUE_ENABLE = ControlItem(64, 1, Dtype.UINT8, "R/W")
    HARDWARE_ERROR_STATUS = ControlItem(70, 1, Dtype.UINT8, "R")
    VELOCITY_I_GAIN = ControlItem(76, 2, Dtype.UINT16, "R/W")
    VELOCITY_P_GAIN = ControlItem(78, 2, Dtype.UINT16, "R/W")
    POSITION_D_GAIN = ControlItem(80, 2, Dtype.UINT16, "R/W")
    POSITION_I_GAIN = ControlItem(82, 2, Dtype.UINT16, "R/W")
    POSITION_P_GAIN = ControlItem(84, 2, Dtype.UINT16, "R/W")
    FEEDFORWARD_ACCELERATION_GAIN = ControlItem(88, 2, Dtype.UINT16, "R/W")
    FEEDFORWARD_VELOCITY_GAIN = ControlItem(90, 2, Dtype.UINT16, "R/W")
    GOAL_PWM = ControlItem(100, 2, Dtype.INT16, "R/W")
    GOAL_CURRENT = ControlItem(102, 2, Dtype.INT16, "R/W")
    GOAL_VELOCITY = ControlItem(104, 4, Dtype.INT32, "R/W")
    PROFILE_ACCELERATION = ControlItem(108, 4, Dtype.UINT32, "R/W")
    PROFILE_VELOCITY = ControlItem(112, 4, Dtype.UINT32, "R/W")
    GOAL_POSITION = ControlItem(116, 4, Dtype.INT32, "R/W")
    REALTIME_TICK = ControlItem(120, 2, Dtype.UINT16, "R")
    MOVING_STATUS = ControlItem(122, 1, Dtype.UINT8, "R")
    PRESENT_PWM = ControlItem(124, 2, Dtype.INT16, "R")
    PRESENT_CURRENT = ControlItem(126, 2, Dtype.INT16, "R")
    PRESENT_VELOCITY = ControlItem(128, 4, Dtype.INT32, "R")
    PRESENT_POSITION = ControlItem(132, 4, Dtype.INT32, "R")
    VELOCITY_TRAJECTORY = ControlItem(136, 4, Dtype.INT32, "R")
    POSITION_TRAJECTORY = ControlItem(140, 4, Dtype.INT32, "R")
    PRESENT_INPUT_VOLTAGE = ControlItem(144, 2, Dtype.UINT16, "R")
    PRESENT_TEMPERATURE = ControlItem(146, 1, Dtype.UINT8, "R")

    def __init__(self, control_item: ControlItem) -> None:
        """
        コントロールテーブルの各項目のデータ構造を設定する.

        これが無いと `ControlTable.BAUDRATE.address` みたいなアクセスができない
        """
        self.address = control_item.address
        self.num_bytes = control_item.num_bytes
        self.dtype = control_item.dtype
        self.access = control_item.access


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
