from __future__ import annotations


class SensibleError(RuntimeError):
    pass


class ValidationError(SensibleError, ValueError):
    pass
