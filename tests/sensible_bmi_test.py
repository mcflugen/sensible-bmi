from __future__ import annotations

import pytest
from sensible_bmi._errors import ValidationError
from sensible_bmi.sensible_bmi import SensibleBmi
from sensible_bmi.sensible_bmi import make_sensible

from tests.utils import DummyBmi


@pytest.fixture
def bmi():
    return DummyBmi()


def test_sensible_bmi_without_bmi():
    class BadBmi(SensibleBmi):
        _cls = None
        _is_initialized = False

    with pytest.raises(RuntimeError, match="There is no BMI"):
        BadBmi()


@pytest.mark.parametrize(
    "name", ["name", "grid", "var", "time", "input_var_names", "output_var_names"]
)
def test_properties_uninitialized(bmi, name):
    Model = make_sensible("Model", DummyBmi)

    model = Model()
    with pytest.raises(ValidationError, match="Model must be initialized"):
        getattr(model, name)
    model.initialize()
    assert getattr(model, name) is not None


def test_update_uninitialized(bmi):
    Model = make_sensible("Model", DummyBmi)

    model = Model()
    with pytest.raises(ValidationError, match="Model must be initialized"):
        model.update()
    model.initialize()
    assert model.update() is None


def test_double_initialize(bmi):
    Model = make_sensible("Model", DummyBmi)

    model = Model()
    model.initialize()
    with pytest.raises(ValidationError, match="Model must not be initialized"):
        model.initialize()
