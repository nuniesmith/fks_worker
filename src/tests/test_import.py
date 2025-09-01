def test_import_worker():
    import importlib, sys, pathlib
    try:
        mod = importlib.import_module("fks_worker.main")
    except ModuleNotFoundError:
        # Fallback for running tests directly from src/ without editable install
        sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
        mod = importlib.import_module("main")
    assert hasattr(mod, "main")
