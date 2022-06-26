import json
from dataclasses import dataclass, asdict
from pathlib import Path

from worldgen import definitions


@dataclass
class ConfigModel:
    model_viewer_executable_path: Path = ''
    automatically_open_model_in_viewer: bool = True


class __ConfigManager:
    __config_model = ConfigModel

    def __init__(self):
        self.config_path: Path = definitions.CONFIG_PATH
        self.load()

    def _config_exists(self) -> bool:
        return self.config_path.exists()

    def _load_config_from_file(self):
        with open(self.config_path, 'r') as f:
            data = json.loads(f.read())
            self.config = self.__config_model(**data)

    def _save_config_to_file(self):
        self._create_config_folder()
        with open(self.config_path, 'w') as f:
            data = asdict(self.config)
            f.write(json.dumps(data))

    def _create_config_folder(self):
        if not self._config_folder_exists():
            self.config_path.parent.mkdir(exist_ok=True, parents=True)

    def _config_folder_exists(self):
        return self.config_path.parent.exists()

    def _create_default_config(self):
        self.config = self.__config_model()

    def load(self):
        if not self._config_exists():
            self._create_default_config()
            self._save_config_to_file()
        self._load_config_from_file()

    def save(self):
        self._save_config_to_file()


config_manager: __ConfigManager = __ConfigManager()
