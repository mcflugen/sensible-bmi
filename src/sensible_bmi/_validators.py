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


def validate_var_dtype(dtype: str, itemsize: int | None = None) -> str:
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


def _normalize_dtype(dtype: str, itemsize: int | None = None) -> str:
    fields = [field.strip() for field in dtype.split(",")]
    if len(fields) > 1:
        return ", ".join(_normalize_dtype(field, itemsize) for field in fields)

    dtype = fields[0]
    if itemsize is None:
        return str(np.dtype(dtype))

    type_map = {
        "float": f"float{itemsize * 8}",
        "complex": f"complex{itemsize * 8}",
        "int": f"int{itemsize * 8}",
        "uint": f"uint{itemsize * 8}",
        "f": f"f{itemsize}",
        "i": f"i{itemsize}",
    }

    return str(np.dtype(type_map.get(dtype, dtype)))


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
