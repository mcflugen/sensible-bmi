from __future__ import annotations

import numpy as np


class DummyBmi:
    """A complete, deterministic BMI implementation for testing."""

    def __init__(self):
        self._initialized = False
        self._time = 0.0

        self._values = {
            "water__depth": np.array([1.0, 2.0, 3.0], dtype=np.float64),
            "land_surface__elevation": np.array([10.0, 20.0, 30.0], dtype=np.float64),
        }

    def get_component_name(self):
        return "dummy component"

    def initialize(self, config_file=None):
        self._initialized = True
        self._time = 0.0

    def finalize(self):
        self._initialized = False

    def update(self):
        self._time += 1.0
        self._values["water__depth"] += 1.0

    def update_until(self, time):
        dt = time - self._time
        self._values["water__depth"] += dt
        self._time = time

    def get_current_time(self):
        return self._time

    def get_start_time(self):
        return 0.0

    def get_end_time(self):
        return 100.0

    def get_time_step(self):
        return 1.0

    def get_time_units(self):
        return "s"

    def get_input_var_names(self):
        return ("water__depth",)

    def get_output_var_names(self):
        return ("water__depth", "land_surface__elevation")

    def get_var_type(self, name):
        return str(self._values[name].dtype)

    def get_var_units(self, name):
        return {
            "water__depth": "m",
            "land_surface__elevation": "m",
        }[name]

    def get_var_location(self, name):
        return "node"

    def get_var_itemsize(self, name):
        return self._values[name].dtype.itemsize

    def get_var_nbytes(self, name):
        return self._values[name].nbytes

    def get_var_grid(self, name):
        return 0

    def get_value_ptr(self, name):
        return self._values[name]

    def get_value(self, name, dest):
        dest[:] = self._values[name]
        return dest

    def set_value(self, name, src):
        self._values[name][:] = src

    def get_grid_rank(self, grid_id):
        return 1

    def get_grid_size(self, grid_id):
        return len(self._values["water__depth"])

    def get_grid_shape(self, grid_id, shape):
        shape[:] = (self.get_grid_size(grid_id),)

    def get_grid_spacing(self, grid_id, spacing):
        spacing[:] = (1.0,)

    def get_grid_origin(self, grid_id, origin):
        origin[:] = (0.0,)

    def get_grid_type(self, grid_id):
        return "uniform_rectilinear"
