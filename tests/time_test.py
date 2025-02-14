from __future__ import annotations

from unittest.mock import Mock

import pytest
from sensible_bmi._time import SensibleTime


def bmi_time(units="s", start=0.0, stop=1.0, step=1.0, current=None):
    mock = Mock()
    mock.get_time_units.return_value = units
    mock.get_start_time.return_value = start
    mock.get_end_time.return_value = stop
    mock.get_time_step.return_value = step
    mock.get_current_time.return_value = start if current is None else current

    return mock


def test_time():
    time = SensibleTime(bmi_time(units="s", start=1.0, stop=10.0, step=0.1))

    assert time.units == "s"
    assert time.start == 1.0
    assert time.stop == 10.0
    assert time.step == 0.1
    assert time.current == time.start


@pytest.mark.parametrize("time_2", (SensibleTime(bmi_time(current=2.0)), 2.0))
def test_comparisons_unequal(time_2):
    time_1 = SensibleTime(bmi_time(current=1.0))

    assert time_1 < time_2
    assert time_1 <= time_2
    assert time_2 > time_1
    assert time_2 >= time_1
    assert time_1 != time_2


@pytest.mark.parametrize("time_2", (SensibleTime(bmi_time(current=2.0)), 2.0))
def test_comparisons_equal(time_2):
    time_1 = SensibleTime(bmi_time(current=2.0))

    assert time_1 <= time_2
    assert time_2 >= time_1
    assert time_1 == time_2


# @pytest.mark.parametrize("bad_value", ("two", True))
@pytest.mark.parametrize("bad_value", ("two", None))
def test_comparison_with_not_time_like(bad_value):
    time = SensibleTime(bmi_time(current=2.0))

    with pytest.raises(TypeError):
        time < bad_value  # noqa: B015
    with pytest.raises(TypeError):
        time > bad_value  # noqa: B015
    with pytest.raises(TypeError):
        time <= bad_value  # noqa: B015
    with pytest.raises(TypeError):
        time >= bad_value  # noqa: B015
    assert not (time == bad_value)
    assert time != bad_value


def test_str():
    time = SensibleTime(bmi_time(units="s", start=1.0, stop=10.0, step=0.1))

    actual = eval(str(time))
    assert actual["units"] == time.units
    assert actual["start"] == time.start
    assert actual["stop"] == time.stop
    assert actual["step"] == time.step


def test_repr():
    time = SensibleTime(bmi_time(units="s", start=1.0, stop=10.0, step=0.1))

    actual = repr(time)
    assert actual.startswith("SensibleTime(") and actual.endswith(")")
