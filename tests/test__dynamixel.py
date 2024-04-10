# ruff: noqa: S101, N802, ARG001
"""`utils.py`のユニットテスト."""

from __future__ import annotations

from textwrap import dedent

import pytest
from robopy import DynamixelCommError


def test__dynamixel_comm_error() -> None:
    """`DynamixelCommError`のテスト."""
    with pytest.raises(DynamixelCommError) as e:
        raise DynamixelCommError(
            message="Test message",
            dxl_comm_result_code=-1002,
            dxl_error_code=4,
        )
    assert str(e.value) == dedent(
        """\
        Test message
        dxl_comm_result='[TxRxResult] Failed get status packet from device!'
        dxl_error='[RxPacketError] The data value is out of range!'"""
    )
