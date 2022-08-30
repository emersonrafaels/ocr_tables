import os

from dynaconf import Dynaconf, settings

os.environ["ENV_FOR_DYNACONF"] = "development"
os.environ[
    "SETTINGS_FILE_FOR_DYNACONF"
] = "src/CONFIG/settings.toml;src/CONFIG/.secrets.toml"
