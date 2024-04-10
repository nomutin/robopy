# ruff: noqa: S101, PLR2004
"""`control_table.py`のユニットテスト."""

import pytest

from robopy.control_table import ControlTable, Dtype, cast_value


def test__control_table() -> None:
    """
    `ControlTable`のテスト.

    各属性への直接アクセスが可能であることを確認する.
    """
    example_table = ControlTable.BAUDRATE
    assert isinstance(example_table, ControlTable)
    assert example_table.address == 8
    assert example_table.num_bytes == 1
    assert example_table.dtype == Dtype.UINT8
    assert example_table.access == "R/W(NVM)"


@pytest.mark.parametrize(
    ("value", "dtype", "expected"),
    [
        ((2**8) ** 0 + 1, Dtype.UINT8, 2),
        ((2**8) ** 1 + 1, Dtype.UINT8, 1),
        ((2**8) ** 2 + 1, Dtype.UINT8, 1),
        ((2**16) ** 0 + 1, Dtype.UINT16, 2),
        ((2**16) ** 1 + 1, Dtype.UINT16, 1),
        ((2**16) ** 2 + 1, Dtype.UINT16, 1),
        ((2**32) ** 0 + 1, Dtype.UINT32, 2),
        ((2**32) ** 1 + 1, Dtype.UINT32, 1),
        ((2**32) ** 2 + 1, Dtype.UINT32, 1),
        ((2**15) ** 0 + 1, Dtype.INT16, 2),
        ((2**15) ** 1 + 1, Dtype.INT16, -(2**15) + 1),
        ((2**16) ** 2 + 1, Dtype.INT16, 1),
        ((2**31) ** 0 + 1, Dtype.INT32, 2),
        ((2**31) ** 1 + 1, Dtype.INT32, -(2**31) + 1),
        ((2**32) ** 2 + 1, Dtype.INT32, 1),
    ],
)
def test__cast_value(value: int, dtype: Dtype, expected: int) -> None:
    """
    `cast_value`のテスト.

    指定されたデータ型に従って値が正規化されているかを確認する.
    """
    assert cast_value(value, dtype) == expected
