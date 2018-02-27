import importlib
import os

_settings = None

def get_settings():
    global _settings
    if not _settings:
        import_path = os.environ.get('SETTINGS_IMPORT_PATH', 'settings')
        _settings = importlib.import_module(import_path)
    return _settings
