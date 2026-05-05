import pytest
import tempfile
import shutil
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config_loader import Config
from core.datastore import JSONDatastore

# Store original config to restore after tests
_original_config_instance = None

@pytest.fixture(autouse=True)
def isolated_datastore(monkeypatch):
    """Ensure each test gets a fresh datastore in a temp directory."""
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())
    
    # Patch Config.load to use temp paths
    original_load = Config.load
    
    def patched_load(path="config/config.yaml"):
        global _original_config_instance
        if _original_config_instance is None:
            _original_config_instance = original_load(path)
        
        # Create a modified config with temp paths
        from config.config_loader import DespachoConfig, DatastoreConfig
        
        temp_data = temp_dir / "data"
        temp_backup = temp_dir / "backups"
        
        return Config(
            version="2.0",
            despacho=_original_config_instance.despacho,
            datastore=DatastoreConfig(
                type="json",
                path=temp_data,
                backup_dir=temp_backup,
            ),
            ids=_original_config_instance.ids,
            motor_kami=_original_config_instance.motor_kami,
            google_workspace=_original_config_instance.google_workspace,
            auth=_original_config_instance.auth,
            notifications=_original_config_instance.notifications
        )
    
    monkeypatch.setattr(Config, "load", patched_load)
    
    # Re-import app to pick up the patched config
    import dashboard.backend.app as app_module
    import importlib
    importlib.reload(app_module)
    
    yield
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def client():
    from dashboard.backend.app import app
    from fastapi.testclient import TestClient
    return TestClient(app)
