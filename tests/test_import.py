def test_worker_import():
    import importlib
    m = importlib.import_module('main')
    assert hasattr(m, 'main')
