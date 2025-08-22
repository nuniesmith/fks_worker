def test_import_worker():
    import importlib
    mod = importlib.import_module("fks_worker.main")
    assert mod is not None
