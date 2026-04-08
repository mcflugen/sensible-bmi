from __future__ import annotations

import numpy as np
import requireit
from sensible_bmi._errors import ValidationError

VALID_VAR_LOCATIONS = frozenset({"node", "edge", "face", "none"})
VALID_GRID_TYPES = frozenset(
    {
        "points",
        "rectilinear",
        "structured_quadrilateral",
        "uniform_rectilinear",
        "unstructured",
    }
)


def validate_var_dtype(dtype: str, itemsize: int | None = None) -> str:
    if not isinstance(dtype, str):
        raise TypeError(f"dtype must be a string, got {type(dtype).__name__}")

    if itemsize is not None:
        itemsize = validate_positive_integer(itemsize, name="itemsize")

    normed_dtype = _normalize_dtype_string(dtype, itemsize)
    try:
        normed_dtype = np.dtype(normed_dtype)
    except (TypeError, ValueError):
        raise ValidationError(
            f"dtype must be a valid BMI variable type, got {dtype!r}"
        ) from None

    return normed_dtype


def _normalize_dtype_string(dtype: str, itemsize: int | None = None) -> str:
    parts = _split_dtype_fields(dtype)
    normalized = [_normalize_dtype_token(part, itemsize=itemsize) for part in parts]
    return ", ".join(normalized)


def _split_dtype_fields(dtype: str) -> list[str]:
    parts = [part.strip() for part in dtype.split(",")]

    if any(part == "" for part in parts):
        raise ValidationError("dtype field must not be empty")

    return parts


def _normalize_dtype_token(dtype: str, itemsize: int | None = None) -> str:
    if itemsize is None:
        return dtype

    if dtype in {"float", "complex", "int", "uint"}:
        return f"{dtype}{itemsize * 8}"

    if dtype in {"f", "i"}:
        return f"{dtype}{itemsize}"

    return dtype


def validate_var_location(location: str) -> str:
    if not isinstance(location, str):
        raise ValidationError("location must be a string")

    try:
        return requireit.require_one_of(
            location.strip().lower(), allowed=VALID_VAR_LOCATIONS, name="location"
        )
    except requireit.ValidationError as err:
        raise ValidationError(str(err)) from None


def validate_positive_integer(value: int, name: str | None = None) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{'value' if name is None else name} must be an integer")

    try:
        return requireit.require_greater_than(value, 0, name=name)
    except requireit.ValidationError as err:
        raise ValidationError(str(err)) from None


def validate_grid_type(type_str: str) -> str:
    if not isinstance(type_str, str):
        raise ValidationError("grid_type must be a string")

    try:
        return requireit.require_one_of(
            type_str.strip().lower(), allowed=VALID_GRID_TYPES, name="grid_type"
        )
    except requireit.ValidationError as err:
        raise ValidationError(str(err)) from None
