from __future__ import annotations

import numpy as np
import pytest
from sensible_bmi._errors import ValidationError
from sensible_bmi._validators import VALID_GRID_TYPES
from sensible_bmi._validators import VALID_VAR_LOCATIONS
from sensible_bmi._validators import validate_grid_rank
from sensible_bmi._validators import validate_grid_type
from sensible_bmi._validators import validate_var_dtype
from sensible_bmi._validators import validate_var_itemsize
from sensible_bmi._validators import validate_var_location
from sensible_bmi._validators import validate_var_nbytes


@pytest.mark.parametrize("value", (1, 10, 100))
def test_grid_rank(value):
    assert validate_grid_rank(value) == value


@pytest.mark.parametrize(
    "value, err", ((0, ValidationError), (-1, ValidationError), (1.0, TypeError))
)
def test_grid_rank_bad_value(value, err):
    with pytest.raises(err):
        validate_grid_rank(value)


@pytest.mark.parametrize(
    "value", sorted(VALID_GRID_TYPES | {t.upper() for t in VALID_GRID_TYPES})
)
def test_grid_type(value):
    assert validate_grid_type(value) == value.lower()


@pytest.mark.parametrize("value", ("foo", ""))
def test_grid_type_bad_value(value):
    with pytest.raises(ValidationError):
        validate_grid_type(value)


@pytest.mark.parametrize("value", (1, 10, 100))
def test_var_nbytes(value):
    assert validate_var_nbytes(value) == value


@pytest.mark.parametrize(
    "value, err",
    (
        (0, ValidationError),
        (-1, ValidationError),
        (1.0, TypeError),
    ),
)
def test_var_nbytes_bad_value(value, err):
    with pytest.raises(err):
        validate_var_nbytes(value)


@pytest.mark.parametrize("value", (1, 10, 100))
def test_var_itemsize(value):
    assert validate_var_itemsize(value) == value


@pytest.mark.parametrize(
    "value, err",
    (
        (0, ValidationError),
        (-1, ValidationError),
        (1.0, TypeError),
    ),
)
def test_var_itemsize_bad_value(value, err):
    with pytest.raises(err):
        validate_var_itemsize(value)


@pytest.mark.parametrize(
    "value", sorted(VALID_VAR_LOCATIONS | {t.upper() for t in VALID_VAR_LOCATIONS})
)
def test_var_location(value):
    assert validate_var_location(value) == value.lower()


@pytest.mark.parametrize("value", ("foo", ""))
def test_var_location_bad_value(value):
    with pytest.raises(ValidationError):
        validate_var_location(value)


@pytest.mark.parametrize(
    "dtype,itemsize,expected",
    [
        ("float", 4, "float32"),
        ("float", 8, "float64"),
        ("complex", 8, "complex64"),
        ("complex", 16, "complex128"),
        ("int", 1, "int8"),
        ("int", 4, "int32"),
        ("uint", 2, "uint16"),
        ("f", 4, "float32"),
        ("i", 2, "int16"),
        ("float32", 4, "float32"),
        ("int16", 2, "int16"),
        ("f4, i2", 4, "float32, int16"),
        ("float, float", 4, "float32, float32"),
        ("float, double", 8, "float64, float64"),
    ],
)
def test_validate_var_dtype_valid(dtype, itemsize, expected):
    result = validate_var_dtype(dtype, itemsize)
    assert result == expected


@pytest.mark.parametrize(
    "dtype,itemsize", [(None, 4), (123, 4), ([], 4), (np.float64, 8)]
)
def test_validate_var_dtype_type_error(dtype, itemsize):
    with pytest.raises(TypeError):
        validate_var_dtype(dtype, itemsize)


@pytest.mark.parametrize(
    "dtype,itemsize", [("nonsense", 4), ("badtype, float32", 4), ("i7", 1)]
)
def test_validate_var_dtype_validation_error(dtype, itemsize):
    with pytest.raises(ValidationError):
        validate_var_dtype(dtype, itemsize)
