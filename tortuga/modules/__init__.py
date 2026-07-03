import os
import importlib

def load_modules():
    """Dynamically load all Python files in this directory to register their actions."""
    mod_dir = os.path.dirname(__file__)
    for filename in os.listdir(mod_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            mod_name = f"tortuga.modules.{filename[:-3]}"
            importlib.import_module(mod_name)
