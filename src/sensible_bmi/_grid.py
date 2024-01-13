from __future__ import annotations

import ctypes
import pprint

import numpy as np
from bmipy.bmi import Bmi
from numpy.typing import NDArray


class SensibleGrid:
    def __init__(self, bmi: Bmi, grid: int):
        self._id = grid
        self._rank = bmi.get_grid_rank(grid)
        self._size = bmi.get_grid_size(grid)
        self._type = bmi.get_grid_type(grid)

        self._bmi = bmi

    @property
    def id(self) -> int:
        return self._id

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def size(self) -> int:
        return self._size

    @property
    def type(self) -> str:
        return self._type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._bmi!r}, {self._id!r})"

    def __str__(self) -> str:
        return pprint.pformat(
            {
                "id": self.id,
                "rank": self.rank,
                "size": self.size,
                "type": self.type,
            }
        )


class SensiblePointGrid(SensibleGrid):
    def __init__(self, bmi: Bmi, grid: int):
        super().__init__(bmi, grid)

        self._node_count = bmi.get_grid_node_count(grid)

        self._x: NDArray[np.float_]
        self._y: NDArray[np.float_]
        self._z: NDArray[np.float_]

        for dim in ("x", "y", "z")[: self.rank]:
            array = np.empty(self._node_count, dtype=ctypes.c_double)
            getattr(bmi, f"get_grid_{dim}")(grid, array)
            array.setflags(write=False)
            self.__dict__[f"_{dim}"] = array

    @property
    def node_count(self) -> int:
        return self._node_count

    @property
    def x_of_node(self) -> NDArray[np.float_]:
        return self._x

    @property
    def y_of_node(self) -> NDArray[np.float_]:
        return self._y

    @property
    def z_of_node(self) -> NDArray[np.float_]:
        return self._z


class SensibleUniformRectilinearGrid(SensibleGrid):
    def __init__(self, bmi: Bmi, grid: int):
        super().__init__(bmi, grid)

        shape = np.empty(self.rank, dtype=ctypes.c_int)
        bmi.get_grid_shape(grid, shape)
        self._shape = tuple(shape)

        spacing = np.empty(self.rank, dtype=ctypes.c_double)
        bmi.get_grid_spacing(grid, spacing)
        self._spacing = tuple(spacing)

        origin = np.empty(self.rank, dtype=ctypes.c_double)
        bmi.get_grid_origin(grid, origin)
        self._origin = tuple(origin)

    @property
    def shape(self) -> tuple[int, ...]:
        return self._shape

    @property
    def spacing(self) -> tuple[float, ...]:
        return self._shape

    @property
    def origin(self) -> tuple[float, ...]:
        return self._origin


class SensibleRectilinearGrid(SensibleGrid):
    def __init__(self, bmi: Bmi, grid: int):
        super().__init__(bmi, grid)

        shape = np.empty(self.rank, dtype=ctypes.c_int)
        bmi.get_grid_shape(grid, shape)
        self._shape: tuple[int, ...] = tuple(shape)

        self._x: NDArray[np.float_]
        self._y: NDArray[np.float_]
        self._z: NDArray[np.float_]

        for dim, name in enumerate(("x", "y", "z")[: self.rank]):
            array = np.empty(self._shape[dim], dtype=ctypes.c_double)
            getattr(bmi, f"get_grid_{name}")(grid, array)
            array.setflags(write=False)
            self.__dict__[f"_{name}"] = array

    @property
    def shape(self) -> tuple[int, ...]:
        return self._shape

    @property
    def x_of_node(self) -> NDArray[np.float_]:
        return self._x

    @property
    def y_of_node(self) -> NDArray[np.float_]:
        return self._y

    @property
    def z_of_node(self) -> NDArray[np.float_]:
        return self._z


class SensibleStructuredQuadrilateralGrid(SensibleGrid):
    def __init__(self, bmi: Bmi, grid: int):
        super().__init__(bmi, grid)

        shape = np.empty(self.rank, dtype=ctypes.c_int)
        bmi.get_grid_shape(grid, shape)
        self._shape = tuple(shape)

        self._node_count = np.prod(shape)

        self._x: NDArray[np.float_]
        self._y: NDArray[np.float_]
        self._z: NDArray[np.float_]

        for dim in ("x", "y", "z")[: self.rank]:
            array = np.empty(self._node_count, dtype=ctypes.c_double)
            getattr(bmi, f"get_grid_{dim}")(grid, array)
            array.setflags(write=False)
            self.__dict__[f"_{dim}"] = array

    @property
    def shape(self) -> tuple[int, ...]:
        return self._shape

    @property
    def x_of_node(self) -> NDArray[np.float_]:
        return self._x

    @property
    def y_of_node(self) -> NDArray[np.float_]:
        return self._y

    @property
    def z_of_node(self) -> NDArray[np.float_]:
        return self._z


class SensibleUnstructuredGrid(SensibleGrid):
    def __init__(self, bmi: Bmi, grid: int):
        super().__init__(bmi, grid)

        self._node_count = bmi.get_grid_node_count(grid)
        self._edge_count = bmi.get_grid_edge_count(grid)
        self._face_count = bmi.get_grid_face_count(grid)

        self._x: NDArray[np.float_]
        self._y: NDArray[np.float_]
        self._z: NDArray[np.float_]

        for dim in ("x", "y", "z")[: self.rank]:
            array = np.empty(self._node_count, dtype=ctypes.c_double)
            getattr(bmi, f"get_grid_{dim}")(grid, array)
            array.setflags(write=False)
            self.__dict__[f"_{dim}"] = array

        self._edge_nodes = np.empty((self.edge_count, 2), dtype=ctypes.c_int)
        bmi.get_edge_nodes(grid, self._edge_nodes.reshape(-1))
        self._edge_nodes.setflags(write=False)

        self._nodes_per_face = np.empty(self._face_count, dtype=ctypes.c_int)
        bmi.get_nodes_per_face(grid, self._nodes_per_face)
        self._nodes_per_face.setflags(write=False)

        self._face_nodes = np.empty(self._nodes_per_face.sum(), dtype=ctypes.c_int)
        bmi.get_face_nodes(grid, self._face_nodes)
        self._face_nodes.setflags(write=False)

        self._face_edges = np.empty(
            (self._nodes_per_face - 1).sum(), dtype=ctypes.c_int
        )
        bmi.get_face_edges(grid, self._face_edges)
        self._face_edges.setflags(write=False)

    @property
    def node_count(self) -> int:
        return self._node_count

    @property
    def edge_count(self) -> int:
        return self._edge_count

    @property
    def face_count(self) -> int:
        return self._face_count

    @property
    def x_of_node(self) -> NDArray[np.float_]:
        return self._x

    @property
    def y_of_node(self) -> NDArray[np.float_]:
        return self._y

    @property
    def z_of_node(self) -> NDArray[np.float_]:
        return self._z

    @property
    def nodes_per_face(self) -> NDArray[np.int_]:
        return self._nodes_per_face

    @property
    def edge_nodes(self) -> NDArray[np.float_]:
        return self._edge_nodes

    @property
    def face_nodes(self) -> NDArray[np.float_]:
        return self._face_nodes

    @property
    def face_edges(self) -> NDArray[np.float_]:
        return self._face_edges


_GRID_CLASS = {
    "points": SensiblePointGrid,
    "uniform_rectilinear": SensibleUniformRectilinearGrid,
    "structured_quadrilateral": SensibleStructuredQuadrilateralGrid,
    "rectilinear": SensibleRectilinearGrid,
    "unstructured": SensibleUnstructuredGrid,
}


def sensible_grid(bmi: Bmi, grid_id: int) -> SensibleGrid:
    grid_type: str = bmi.get_grid_type(grid_id)
    return _GRID_CLASS[grid_type](bmi, grid_id)
