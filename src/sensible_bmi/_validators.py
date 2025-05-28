from __future__ import annotations

import numpy as np
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


def validate_var_dtype(dtype: str, itemsize: int) -> str:
    if not isinstance(dtype, str):
        raise TypeError(f"dtype must be a string, got {type(dtype).__name__}")

    try:
        normed_dtype = _normalize_dtype(dtype, itemsize)
        np.dtype(normed_dtype)
    except (TypeError, ValueError):
        raise ValidationError(
            f"invalid string for BMI variable type ({dtype!r})"
        ) from None
    return normed_dtype


def _normalize_dtype(dtype: str, itemsize: int) -> str:
    fields = [field.strip() for field in dtype.split(",")]
    if len(fields) == 1:
        dtype = fields[0]
        if dtype in ("float", "complex", "int", "uint"):
            dtype = f"{dtype}{itemsize * 8}"
        elif dtype in ("f", "i"):
            dtype = f"{dtype}{itemsize}"
        return str(np.dtype(dtype))
    else:
        return ", ".join(_normalize_dtype(field, itemsize) for field in fields)


def validate_var_location(location: str) -> str:
    location = location.strip().lower()
    if location not in VALID_VAR_LOCATIONS:
        raise ValidationError(
            f"{location!r}: invalid BMI variable location"
            f" (not one of {', '.join(sorted(VALID_VAR_LOCATIONS))})"
        )
    return location


def validate_var_itemsize(size: int) -> int:
    if not isinstance(size, int):
        raise TypeError(f"{size}: itemsize must be integer")
    if size <= 0:
        raise ValidationError(f"{size}: itemsize must be a positive integer")
    return size


def validate_var_nbytes(nbytes: int) -> int:
    if not isinstance(nbytes, int):
        raise TypeError(f"{nbytes}: nbytes must be integer")
    if nbytes <= 0:
        raise ValidationError(f"{nbytes}: nbytes must be a positive integer")
    return nbytes


def validate_grid_rank(rank: int) -> int:
    if not isinstance(rank, int):
        raise TypeError(f"{rank}: rank must be integer")
    if rank <= 0:
        raise ValidationError(f"{rank}: rank must be a positive integer")
    return rank


def validate_grid_type(type_str: str) -> str:
    type_str = type_str.strip().lower()
    if type_str not in VALID_GRID_TYPES:
        raise ValidationError(
            f"{type_str!r}: invalid BMI grid type"
            f" (not one of {', '.join(sorted(VALID_GRID_TYPES))})"
        )
    return type_str
