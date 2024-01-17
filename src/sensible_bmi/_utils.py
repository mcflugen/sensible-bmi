from __future__ import annotations

import contextlib
import os
from collections.abc import Callable
from collections.abc import Generator
from functools import wraps
from typing import Any

from sensible_bmi._errors import SensibleError


def is_initialized_or_raise(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: Any, *args: tuple[Any], **kwds: dict[str, Any]) -> Any:
        try:
            self._initdir
        except AttributeError:
            raise SensibleError(
                f"`{self.__class__.__name__}.{func.__name__}` is not available until"
                " this component has been initialized."
                " Did you forget to run initialize?"
            ) from None
        return func(self, *args, **kwds)

    return wrapper


@contextlib.contextmanager
def as_cwd(path: str) -> Generator[str, None, None]:
    prev_cwd = os.getcwd()
    os.chdir(path)
    yield prev_cwd
    os.chdir(prev_cwd)
