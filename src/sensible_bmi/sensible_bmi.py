from __future__ import annotations

import os
from types import MappingProxyType

from bmipy.bmi import Bmi
from sensible_bmi._errors import SensibleError
from sensible_bmi._grid import sensible_grid
from sensible_bmi._grid import SensibleGrid
from sensible_bmi._time import SensibleTime
from sensible_bmi._utils import as_cwd
from sensible_bmi._utils import is_initialized_or_raise
from sensible_bmi._var import SensibleInputOutputVar
from sensible_bmi._var import SensibleInputVar
from sensible_bmi._var import SensibleOutputVar
from sensible_bmi._var import SensibleVar


def make_sensible(class_name: str, bmi_class: type[Bmi]) -> type[SensibleBmi]:
    """Give a BMI component a more sensible interface.

    Parameters
    ----------
    class_name : str
        The name of the new class.
    bmi_class : type
        The BMI class to wrap.

    Returns
    -------
    type
        A new class that wraps the BMI class.
    """
    return type(class_name, (SensibleBmi,), {"_cls": bmi_class})


class SensibleBmi:
    _cls: type[Bmi] | None = None

    def __init__(self) -> None:
        if self._cls is None:
            raise RuntimeError("There is no BMI class associated with this class.")

        self._bmi = self._cls()

        self._initdir: str
        self._name: str
        self._grid: MappingProxyType[int, SensibleGrid]
        self._var: MappingProxyType[str, SensibleVar]
        self._time: SensibleTime
        self._input_var_names: frozenset[str]
        self._output_var_names: frozenset[str]

    def initialize(self, filepath: str | None = None, where: str | None = ".") -> None:
        """Initialize component for timestepping.

        Parameters
        ----------
        filepath : str, optional
            The name of the component's input file.
        where : str, optional
            The path to the location where this component will be run. If not
            provided, use the folder in which *filepath* sits. If *filepath* is also
            not provided, use the current working directory.
        """
        if hasattr(self, "_initdir"):
            raise SensibleError(
                "Unable to initialize. Component is already initialized."
                " If you would like to re-initialize this component, try"
                " calling finalize() and then calling initialize()."
            )

        filepath = "" if filepath is None else os.path.abspath(filepath)

        if filepath and where is None:
            where = os.path.dirname(filepath)
        else:
            where = "." if where is None else where

        init_dir = os.path.abspath(where)
        with as_cwd(init_dir):
            self.bmi.initialize(filepath)

        self._name = self.bmi.get_component_name()
        self._input_var_names = frozenset(self._bmi.get_input_var_names())
        self._output_var_names = frozenset(self._bmi.get_output_var_names())

        all_vars = self._output_var_names | self._input_var_names
        all_grids = {
            self._bmi.get_var_grid(name)
            for name in all_vars
            if self._bmi.get_var_location(name) != "none"
        }

        self._grid = MappingProxyType(
            {grid_id: sensible_grid(self._bmi, grid_id) for grid_id in all_grids}
        )

        self._var = MappingProxyType(
            {
                name: SensibleOutputVar(self._bmi, name)
                for name in self._output_var_names - self._input_var_names
            }
            | {
                name: SensibleInputVar(self._bmi, name)
                for name in self._input_var_names - self._output_var_names
            }
            | {
                name: SensibleInputOutputVar(self._bmi, name)
                for name in self._output_var_names & self._input_var_names
            }
        )

        self._time = SensibleTime(self._bmi)
        self._initdir = init_dir

    @is_initialized_or_raise
    def update(self) -> None:
        """Update the component by a single time step."""
        with as_cwd(self._initdir):
            return self.bmi.update()

    def finalize(self) -> None:
        """Call teardown methods putting the component in a state to be initialized."""
        try:
            self._initdir
        except AttributeError:
            pass
        else:
            with as_cwd(self._initdir):
                self.bmi.finalize()
            del self._initdir

    @property
    def bmi(self) -> Bmi:
        """The underlying BMI of the component."""
        return self._bmi

    @property
    @is_initialized_or_raise
    def name(self) -> str:
        """Name of the component."""
        return self._name

    @property
    @is_initialized_or_raise
    def grid(self) -> MappingProxyType[int, SensibleGrid]:
        """Descriptions of the component's grids."""
        return self._grid

    @property
    @is_initialized_or_raise
    def var(self) -> MappingProxyType[str, SensibleVar]:
        """The component's input and output variables."""
        return self._var

    @property
    @is_initialized_or_raise
    def time(self) -> SensibleTime:
        """Time information about the component."""
        return self._time

    @property
    @is_initialized_or_raise
    def input_var_names(self) -> frozenset[str]:
        """List of the input variables."""
        return self._input_var_names

    @property
    @is_initialized_or_raise
    def output_var_names(self) -> frozenset[str]:
        """List of the output variables."""
        return self._output_var_names
