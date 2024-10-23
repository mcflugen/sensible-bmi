# A Sensible BMI from humans

Enhancing the interoperability, reusability, and integration of diverse computational
models in Earth system sciences (and beyond!), the Basic Model Interface is a worderful
thing.

Let's face it, though, the BMI can be somewhat cumbersome when used directly by humans.

As an example of this, the following code is what is required to get an array of
values from a model that implements a BMI.

```python
dtype = bmi_model.get_var_type(var_name)
itemsize = bmi_model.get_var_itemsize(var_name)
nbytes = bmi_model.get_var_nbytes(var_name)
size = nbytes // itemsize
values = np.empty(size, dtype=self._type)
bmi_model.get_value(var_name, values)
```

*sensible_bmi* helps to humanize a BMI-model. With a model that has been wrapped
with a *SensibleBmi*, the above code becomes,

```python
values = sensible_bmi.var[var_name].get()
```

Below are some examples of common tasks written using both the `SensibleBmi` and
the `BMI`.

:::::{dropdown} Create
:open:

::::{tab-set}
:sync-group: sensible

:::{tab-item} Sensible
:sync: sensible

```python
from bmi_model import BmiModel
from sensible_bmi.sensible_bmi import make_sensible

SensibleBmiModel = make_sensible("SensibleBmiModel", BmiModel)
sensible_bmi = SensibleBmiModel()
```
:::

:::{tab-item} BMI
:sync: not-sensible

```python
from bmi_model import BmiModel

bmi_model = BmiModel()
```
:::
::::
:::::

:::::{dropdown} Get values

::::{tab-set}
:sync-group: sensible

:::{tab-item} Sensible
:sync: sensible

```python
values = sensible_bmi.var[var_name].get()
```
:::

:::{tab-item} BMI
:sync: not-sensible

```python
dtype = bmi_model.get_var_type(var_name)
itemsize = bmi_model.get_var_itemsize(var_name)
nbytes = bmi_model.get_var_nbytes(var_name)
size = nbytes // itemsize
values = np.empty(size, dtype=self._type)
bmi_model.get_value(var_name, values)
```
:::
::::
:::::

:::::{dropdown} Set values
::::{tab-set}
:sync-group: sensible

:::{tab-item} Sensible
:sync: sensible

```python
values = sensible_bmi.var[var_name].set(1.0)
```
:::

:::{tab-item} BMI
:sync: not-sensible

```python
dtype = bmi_model.get_var_type(var_name)
itemsize = bmi_model.get_var_itemsize(var_name)
nbytes = bmi_model.get_var_nbytes(var_name)
size = nbytes // itemsize
values = np.ones(size, dtype=self._type)
bmi_model.set_value(var_name, values)
```
:::
::::
:::::


:::::{dropdown} Grid
::::{tab-set}
:sync-group: sensible

:::{tab-item} Sensible
:sync: sensible

```python
sensible_bmi.var[var_name].grid.shape
sensible_bmi.var[var_name].grid.spacing
```
:::

:::{tab-item} BMI
:sync: not-sensible

```python
grid_id = bmi_model.get_var_grid(var_name)
rank = bmi_model.get_grid_rank(grid_id)

shape = np.ndarray(rank, dtype=int)
spacing = np.ndarray(rank, dtype=float)

bmi_model.get_grid_shape(grid_id, shape)
bmi_model.get_grid_spacing(grid_id, spacing)
```
::::
:::::

:::::{dropdown} Time
::::{tab-set}
:sync-group: sensible

:::{tab-item} Sensible
:sync: sensible

```python
sensible_bmi.time.start
sensible_bmi.time.stop
sensible_bmi.time.current
sensible_bmi.time.step
sensible_bmi.time.units
```
:::

:::{tab-item} BMI
:sync: not-sensible

```python
bmi_model.get_start_time()
bmi_model.get_end_time()
bmi_model.get_current_time()
bmi_model.get_time_step()
bmi_model.get_time_units()
```
::::
:::::
