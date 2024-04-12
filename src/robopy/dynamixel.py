"""
Dynamixel サーボモータの制御.

References
----------
- [AlexanderKoch-Koch/low_cost_robot](https://github.com/AlexanderKoch-Koch/low_cost_robot)
- [wuphilipp/gello_software](https://github.com/wuphilipp/gello_software)
"""

import dynamixel_sdk

from robopy.control_table import ControlTable, cast_value


class DynamixelDriver:
    """Dynamixelを1個単位で制御するためのクラス."""

    def __init__(
        self,
        servo_id: int,
        port_handler: dynamixel_sdk.PortHandler,
        packet_handler: dynamixel_sdk.Protocol2PacketHandler,
    ) -> None:
        """
        通信のためのハンドラ等を設定する.

        Parameters
        ----------
        servo_id : int
            DynamixelのID.
        port_handler : PortHandler
            シリアル通信のためのハンドラ.
        packet_handler : Protocol2PacketHandler
            パケットのためのハンドラ.

        """
        self.servo_id = servo_id
        self.port_handler = port_handler
        self.packet_handler = packet_handler

    def read(self, control_table: ControlTable) -> int:
        """
        Dynamixelからデータを読み取る.

        パケットハンドラから取得した値を `cast_value` で有効な値に加工して返す.

        Example
        -------
        ```python
        from robopy import DynamixelDriver, ControlTable

        dynamixel = DynamixelDriver(...)
        while True:
            value = dynamixel.read(ControlTable.PRESENT_POSITION)
            print(f"Current position: {value}")
        ```

        Parameters
        ----------
        control_table : ControlTable
            読み取るデータの `ControlTable`.

        Returns
        -------
        int
            取得した値. `ControlTable`の内容に従った整数値.

        Raises
        ------
        DynamixelCommError
            読み込みに失敗した場合.

        """
        read_functions = {
            1: self.packet_handler.read1ByteTxRx,
            2: self.packet_handler.read2ByteTxRx,
            4: self.packet_handler.read4ByteTxRx,
        }
        read_func = read_functions[control_table.num_bytes]

        value, dxl_comm_result, dxl_error = read_func(
            port=self.port_handler,
            dxl_id=self.servo_id,
            address=control_table.address,
        )
        if dxl_comm_result == dynamixel_sdk.COMM_SUCCESS:
            return cast_value(value, dtype=control_table.dtype)

        msg = f"{self.servo_id=}の{control_table}の読み取りに失敗しました."
        raise DynamixelCommError(msg, dxl_comm_result, dxl_error)

    def write(self, control_table: ControlTable, value: int) -> None:
        """
        Dynamixelにデータを書き込む.

        Example
        -------
        ```python
        from robopy import DynamixelDriver, ControlTable

        dynamixel = DynamixelDriver(...)
        dynamixel.write(ControlTable.TORQUE_ENABLE, 1)
        ```

        Parameters
        ----------
        control_table : ControlTable
            書き込むデータの種類.
        value : int
            書き込む値.

        Returns
        -------
        None

        Raises
        ------
        DynamixelCommError
            通信に失敗した場合.
            read-onlyの場合やトルク有効時のnvmへの書き込みも含む.

        """
        write_functions = {
            1: self.packet_handler.write1ByteTxRx,
            2: self.packet_handler.write2ByteTxRx,
            4: self.packet_handler.write4ByteTxRx,
        }
        write_func = write_functions[control_table.num_bytes]
        dxl_comm_result, dxl_error = write_func(
            port=self.port_handler,
            dxl_id=self.servo_id,
            address=control_table.address,
            data=value,
        )
        if dxl_comm_result == dynamixel_sdk.COMM_SUCCESS:
            return

        msg = f"{self.servo_id=}の{control_table}の書き込みに失敗しました."
        raise DynamixelCommError(msg, dxl_comm_result, dxl_error)


class DynamixelCommError(ConnectionError):
    """
    Dynamixelの通信エラーを表す例外.

    `dxl_comm_result_code` と `dxl_error_code` は
    `dynamixel_sdk.packetHandler` のread/write系メソッドの返り値に対応する.

    """

    def __init__(
        self,
        message: str,
        dxl_comm_result_code: int,
        dxl_error_code: int,
    ) -> None:
        """`Protocol2PacketHandler` を使ってエラー内容を取得する."""
        packet_handler = dynamixel_sdk.Protocol2PacketHandler()
        dxl_comm_result = packet_handler.getTxRxResult(dxl_comm_result_code)
        dxl_error = packet_handler.getRxPacketError(dxl_error_code)

        message = message.replace("\n", "") + "\n"
        message += f"{dxl_comm_result=}\n{dxl_error=}"

        super().__init__(message)
