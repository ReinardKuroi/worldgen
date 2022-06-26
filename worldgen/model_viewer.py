import subprocess

from worldgen.config import config_manager


class ModelViewer:
    def __init__(self):
        self.executable = config_manager.config.model_viewer_executable_path

    def model_viewer_is_set(self) -> bool:
        return self.executable

    def model_viewer_exists(self) -> bool:
        return self.executable.exists()

    def open(self, file_path):
        try:
            subprocess.run(f'{self.executable} {file_path}')
        except FileNotFoundError as exc:
            print(f'Failed to open model viewer {self.executable}: {exc}')
