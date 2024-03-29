from __future__ import annotations

import pprint
from typing import Any

import numpy as np
from bmipy.bmi import Bmi
from numpy.typing import NDArray


class SensibleVar:
    def __init__(self, bmi: Bmi, name: str):
        self._name = name
        self._units = bmi.get_var_units(name)
        self._location = bmi.get_var_location(name)
        self._grid = None if self._location == "none" else bmi.get_var_grid(name)
        self._type = bmi.get_var_type(name)
        self._itemsize = bmi.get_var_itemsize(name)
        self._nbytes = bmi.get_var_nbytes(name)
        self._size = self._nbytes // self._itemsize
        self._data = np.empty(self._size, dtype=self._type)
        self._data_read_only = self._data.view()
        self._data_read_only.setflags(write=False)

        self._bmi = bmi

    @property
    def name(self) -> str:
        return self._name

    @property
    def units(self) -> str:
        return self._units

    @property
    def location(self) -> str:
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

    @property
    def data(self) -> NDArray[Any]:
        return self._data_read_only

    def get(self) -> NDArray[Any]:
        self._bmi.get_value(self._name, self._data)
        return self._data_read_only

    def set(self, values: NDArray[Any]) -> None:
        self._bmi.set_value(self._name, np.broadcast_to(values, self._data.shape))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._bmi!r}, {self._name!r})"

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
