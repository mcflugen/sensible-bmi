from __future__ import annotations

import numpy as np
import pytest
from sensible_bmi._grid import SensiblePointGrid
from sensible_bmi._grid import SensibleRectilinearGrid
from sensible_bmi._grid import SensibleStructuredQuadrilateralGrid
from sensible_bmi._grid import SensibleUniformRectilinearGrid

from testing.grids import bmi_points
from testing.grids import bmi_raster
from testing.grids import bmi_rectilinear
from testing.grids import bmi_structured_quad


@pytest.mark.parametrize("rank", (1, 2, 3))
def test_grid_points(rank):
    dims = [np.random.rand(5) for _ in range(rank)]

    grid = SensiblePointGrid(bmi_points(*dims), 10)

    assert grid.id == 10
    assert grid.rank == rank
    assert grid.type == "points"
    assert grid.node_count == 5
    assert all(grid.x_of_node == dims[0])
    if rank > 1:
        assert all(grid.y_of_node == dims[1])
    if rank > 2:
        assert all(grid.z_of_node == dims[2])


@pytest.mark.parametrize("rank", (1, 2, 3))
def test_grid_raster(rank):
    shape = np.random.randint(1, 1024, rank)
    spacing = np.random.rand(rank)
    origin = np.random.rand(rank)
    grid = SensibleUniformRectilinearGrid(bmi_raster(shape, spacing, origin), -1)

    assert grid.id == -1
    assert grid.rank == rank
    assert grid.type == "uniform_rectilinear"
    assert grid.shape == tuple(shape)
    assert grid.spacing == tuple(spacing)
    assert grid.origin == tuple(origin)


@pytest.mark.parametrize("rank", (1, 2, 3))
def test_grid_rectilinear(rank):
    shape = np.random.randint(1, 1024, rank)
    dims = [np.random.rand(shape[dim]) for dim in range(rank)]

    grid = SensibleRectilinearGrid(bmi_rectilinear(*dims), 42)

    assert grid.id == 42
    assert grid.rank == rank
    assert grid.type == "rectilinear"
    assert grid.shape == tuple(shape)
    assert all(grid.x_of_node == dims[rank - 1])
    if rank > 1:
        assert all(grid.y_of_node == dims[rank - 2])
    if rank > 2:
        assert all(grid.z_of_node == dims[rank - 3])


@pytest.mark.parametrize("rank", (1, 2, 3))
def test_grid_structured_quad(rank):
    shape = np.random.randint(1, 64, rank)
    args = [
        arg.flatten()
        for arg in np.meshgrid(*[range(dim) for dim in shape], indexing="ij")
    ]
    grid = SensibleStructuredQuadrilateralGrid(bmi_structured_quad(shape, *args), 0)

    assert grid.rank == rank
    assert grid.type == "structured_quadrilateral"
    assert grid.shape == tuple(shape)
    assert all(grid.x_of_node == args[rank - 1])
    if rank > 1:
        assert all(grid.y_of_node == args[rank - 2])
    if rank > 2:
        assert all(grid.z_of_node == args[rank - 3])
