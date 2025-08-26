from importlib import import_module as _imp
_legacy = _imp("main")  # type: ignore
main = getattr(_legacy, "main")
__all__ = ["main"]