from __future__ import annotations

from unittest.mock import Mock

import numpy as np
import pytest
from numpy.testing import assert_array_equal
from sensible_bmi._var import SensibleInputOutputVar
from sensible_bmi._var import SensibleInputVar
from sensible_bmi._var import SensibleOutputVar


def bmi_var(
    array, units="m", location="node", grid=0, dtype=None, itemsize=None, nbytes=None
):
    mock = Mock()
    mock.get_var_units.return_value = units
    mock.get_var_location.return_value = location
    mock.get_var_grid.return_value = grid
    mock.get_var_type.return_value = str(array.dtype) if dtype is None else str(dtype)
    mock.get_var_itemsize.return_value = (
        array.itemsize if itemsize is None else itemsize
    )
    mock.get_var_nbytes.return_value = array.nbytes if nbytes is None else nbytes

    mock.get_value.side_effect = lambda name, out: np.copyto(out, array)
    mock.set_value.return_value = None

    return mock


@pytest.mark.parametrize(
    "cls", (SensibleInputOutputVar, SensibleOutputVar, SensibleInputVar)
)
def test_var(cls):
    values = np.random.rand(5)
    var = cls(bmi_var(values, units="s", location="edge", grid=2), "foo")

    assert var.name == "foo"
    assert var.units == "s"
    assert var.location == "edge"
    assert var.grid == 2
    assert var.type == "float64"
    assert var.itemsize == 8
    assert var.nbytes == 8 * 5
    assert var.size == 5


@pytest.mark.parametrize("cls", (SensibleInputOutputVar, SensibleOutputVar))
@pytest.mark.parametrize(
    "dtype", ("float", "int", "uint", "uint8", "f4,i2", "f", "B", "bool", "complex")
)
def test_var_out_structured_data(cls, dtype):
    dt = np.dtype(dtype)
    values = np.empty(10, dtype=dt)
    var = cls(
        bmi_var(values, itemsize=dt.itemsize, dtype=dtype, nbytes=dt.itemsize * 10),
        "bar",
    )

    assert var.size == 10
    assert var.itemsize == dt.itemsize
    assert var.nbytes == dt.itemsize * 10
    assert var.get().tobytes() == values.tobytes()
    # with pytest.raises(ValueError):
    #     var.data[0] = 1.0

    array = var.empty()
    assert array.dtype == var.type
    assert array.nbytes == var.nbytes
    assert array.itemsize == var.itemsize
    assert array.size == var.size


@pytest.mark.parametrize("cls", (SensibleInputOutputVar, SensibleOutputVar))
def test_var_out(cls):
    values = np.random.rand(10)
    var = cls(bmi_var(values, itemsize=8, dtype="float64", nbytes=8 * 10), "bar")

    assert var.size == 10
    assert all(var.get() == values)
    # assert all(var.data == values)
    # assert var.get() is not var.data
    # with pytest.raises(ValueError):
    #     var.data[0] = 1.0

    array = var.empty()
    assert array.dtype == var.type
    assert array.nbytes == var.nbytes
    assert array.itemsize == var.itemsize
    assert array.size == var.size


@pytest.mark.parametrize("cls", (SensibleInputVar,))
@pytest.mark.parametrize(
    "dtype", ("float", "int", "uint", "uint8", "f4,i2", "f", "B", "bool", "complex")
)
def test_var_in(cls, dtype):
    # values = np.random.rand(20)
    dt = np.dtype(dtype)
    values = np.empty(10, dtype=dt)
    var = cls(bmi_var(values, dtype=dtype), "bar")

    assert var.name == "bar"
    assert var.size == 10
    with pytest.raises(AttributeError):
        var.get()
    # with pytest.raises(AttributeError):
    #     var.data
    var.set(values)


@pytest.mark.parametrize("cls", (SensibleInputOutputVar, SensibleOutputVar))
@pytest.mark.parametrize(
    "dtype", ("float", "int", "uint", "uint8", "f", "B", "bool", "complex")
)
@pytest.mark.parametrize("func", ("zeros", "ones"))
def test_zeros_and_ones(cls, dtype, func):
    dt = np.dtype(dtype)
    values = np.empty(10, dtype=dt)
    var = cls(
        bmi_var(values, itemsize=dt.itemsize, dtype=dtype, nbytes=dt.itemsize * 10),
        "bar",
    )

    actual = getattr(var, func)()
    assert actual.size == 10
    assert actual.itemsize == dt.itemsize
    assert actual.nbytes == dt.itemsize * 10
    assert np.all(actual == (1 if func == "ones" else 0))


@pytest.mark.parametrize("cls", (SensibleInputOutputVar, SensibleOutputVar))
@pytest.mark.parametrize(
    "dtype", ("float", "int", "uint", "uint8", "f4,i2", "f", "B", "bool", "complex")
)
def test_full(cls, dtype):
    dt = np.dtype(dtype)
    values = np.empty(10, dtype=dt)
    var = cls(
        bmi_var(values, itemsize=dt.itemsize, dtype=dtype, nbytes=dt.itemsize * 10),
        "bar",
    )

    assert_array_equal(var.full(1), var.ones())
    assert_array_equal(var.full(0), var.zeros())
