# A Sensible BMI from humans

Enhancing the interoperability, reusability, and integration of diverse computational
models in Earth system sciences (and beyond!), the Basic Model Interface is a worderful
thing.

Let's face it, though, the BMI can be somewhat cumbersome when used directly by humans.

As an example of this, the following code is what is required to get an array of
values from a model that implements a BMI.

```python
>>> dtype = bmi_model.get_var_type(var_name)
>>> itemsize = bmi_model.get_var_itemsize(var_name)
>>> nbytes = bmi_model.get_var_nbytes(var_name)
>>> size = nbytes // itemsize
>>> values = np.empty(size, dtype=self._type)
>>> bmi_model.get_value(var_name, values)
```

This is fine when used within a framework but it becomes tedious if a human would
like to play with a model interactively.

*sensible_bmi* helps to humanize a BMI-model. With a model that has been wrapped
with a *SensibleBmi*, the above code becomes,

```python
>>> values = sensible_bmi.var[var_name].get()
```

## Usage

Wrap a class that exposes a BMI,

```python
>>> from sensible_bmi.sensible_bmi import make_sensible
>>> EzBmi = make_sensible("EzBmi", MyBMI)
```
