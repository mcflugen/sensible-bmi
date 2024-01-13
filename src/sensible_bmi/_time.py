from __future__ import annotations

import pprint

from bmipy.bmi import Bmi


class SensibleTime:
    def __init__(self, bmi: Bmi):
        self._units = bmi.get_time_units()
        self._start = bmi.get_start_time()
        self._stop = bmi.get_end_time()
        self._step = bmi.get_time_step()

        self._bmi = bmi

    @property
    def units(self) -> str:
        return self._units

    @property
    def start(self) -> float:
        return self._start

    @property
    def stop(self) -> float:
        return self._stop

    @property
    def step(self) -> float:
        return self._step

    @property
    def current(self) -> float:
        return self._bmi.get_current_time()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._bmi!r})"

    def __str__(self) -> str:
        return pprint.pformat(
            {
                "units": self.units,
                "start": self.start,
                "stop": self.stop,
                "step": self.step,
                "current": self.current,
            }
        )
