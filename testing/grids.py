from __future__ import annotations

from unittest.mock import Mock

import numpy as np


def bmi_grid(rank, grid_type):
    mock = Mock()
    mock.get_grid_rank.return_value = rank
    mock.get_grid_type.return_value = grid_type
    return mock


def bmi_points(*args):
    rank = len(args)
    dims = ("x", "y", "z")[:rank]

    mock = Mock()
    mock.get_grid_type.return_value = "points"
    mock.get_grid_rank.return_value = len(args)

    for dim, vals in zip(dims, args):
        getattr(mock, f"get_grid_{dim}").side_effect = (
            lambda grid, array, _v=vals: np.copyto(array, _v)
        )
    mock.get_grid_node_count.return_value = len(args[0])

    return mock


def bmi_raster(shape, spacing, origin):
    rank = len(shape)

    mock = Mock()
    mock.get_grid_type.return_value = "uniform_rectilinear"
    mock.get_grid_rank.return_value = rank
    mock.get_grid_shape.side_effect = lambda grid, array: np.copyto(array, shape)
    mock.get_grid_spacing.side_effect = lambda grid, array: np.copyto(array, spacing)
    mock.get_grid_origin.side_effect = lambda grid, array: np.copyto(array, origin)

    return mock


def bmi_rectilinear(*args):
    rank = len(args)
    dims = ("x", "y", "z")[rank - 1 :: -1]
    shape = [len(vals) for vals in args]

    mock = Mock()
    mock.get_grid_type.return_value = "rectilinear"
    mock.get_grid_rank.return_value = rank
    mock.get_grid_shape.side_effect = lambda grid, array: np.copyto(array, shape)
    for dim, vals in zip(dims, args):
        getattr(mock, f"get_grid_{dim}").side_effect = (
            lambda grid, array, _v=vals: np.copyto(array, _v)
        )

    return mock


def bmi_structured_quad(shape, *args):
    rank = len(shape)
    dims = ("x", "y", "z")[rank - 1 :: -1]

    mock = Mock()
    mock.get_grid_type.return_value = "structured_quadrilateral"
    mock.get_grid_rank.return_value = rank
    mock.get_grid_shape.side_effect = lambda grid, array: np.copyto(array, shape)
    for dim, vals in zip(dims, args):
        getattr(mock, f"get_grid_{dim}").side_effect = (
            lambda grid, array, _v=vals: np.copyto(array, _v)
        )

    return mock
