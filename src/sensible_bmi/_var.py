from __future__ import annotations

import os
import pprint
from typing import Any

import numpy as np
from bmipy.bmi import Bmi
from numpy.typing import ArrayLike
from numpy.typing import NDArray
from sensible_bmi._validators import validate_var_dtype
from sensible_bmi._validators import validate_var_itemsize
from sensible_bmi._validators import validate_var_location
from sensible_bmi._validators import validate_var_nbytes


class SensibleVar:
    def __init__(self, bmi: Bmi, name: str):
        self._bmi = bmi
        self._name = name

        self._units = bmi.get_var_units(name)
        location_str = validate_var_location(bmi.get_var_location(name))
        self._location = None if location_str == "none" else location_str
        self._grid = None if location_str == "none" else bmi.get_var_grid(name)
        self._itemsize = validate_var_itemsize(bmi.get_var_itemsize(name))
        self._type = validate_var_dtype(bmi.get_var_type(name), self._itemsize)
        self._nbytes = validate_var_nbytes(bmi.get_var_nbytes(name))
        self._size = self._nbytes // self._itemsize

    @property
    def name(self) -> str:
        return self._name

    @property
    def units(self) -> str:
        return self._units

    @property
    def location(self) -> str | None:
        return self._location

    @property
    def grid(self) -> int | None:
        return self._grid

    @property
    def type(self) -> str:
        return self._type

    @property
    def itemsize(self) -> int:
        return self._itemsize

    @property
    def nbytes(self) -> int:
        return self._nbytes

    @property
    def size(self) -> int:
        return self._size

    def empty(self) -> NDArray[Any]:
        return np.empty(self._size, dtype=self._type)

    def zeros(self) -> NDArray[Any]:
        return np.zeros(self._size, dtype=self._type)

    def ones(self) -> NDArray[Any]:
        return np.ones(self._size, dtype=self._type)

    def full(self, fill_value: ArrayLike) -> NDArray[Any]:
        return np.full(self._size, fill_value, dtype=self._type)

    def __repr__(self) -> str:
        return os.linesep.join(
            [f"{self.__class__.__name__}({self._bmi!r}, {self._name!r})", str(self)]
        )

    def __str__(self) -> str:
        return pprint.pformat(
            {
                "name": self.name,
                "units": self.units,
                "location": self.location,
                "grid": self.grid,
                "type": self.type,
                "itemsize": self.itemsize,
                "nbytes": self.nbytes,
                "size": self.size,
            }
        )


class SensibleInputVar(SensibleVar):
    def set(self, values: ArrayLike) -> None:
        values = np.asarray(values).reshape(-1)
        self._bmi.set_value(
            self._name, np.broadcast_to(values, self._nbytes // self.itemsize)
        )


class SensibleOutputVar(SensibleVar):
    # @property
    # def data(self) -> NDArray[Any]:
    #     return self._data_read_only

    def get(self, out: NDArray[Any] | None = None) -> NDArray[Any]:
        if out is None:
            out = self.empty()
        self._bmi.get_value(self._name, out)
        return out

    def __str__(self) -> str:
        # with np.printoptions(threshold=6):
        return pprint.pformat(
            {
                "name": self.name,
                "units": self.units,
                "location": self.location,
                "grid": self.grid,
                "type": self.type,
                "itemsize": self.itemsize,
                "nbytes": self.nbytes,
                "size": self.size,
                # "data": self.data,
            }
        )


class SensibleInputOutputVar(SensibleInputVar, SensibleOutputVar):
    pass
