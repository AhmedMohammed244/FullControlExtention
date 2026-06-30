from pathlib import Path
from urllib.parse import urlparse
import shutil
import requests

from models.task import Task


class InputLoader:

    def __init__(self):
        self.workspace = Path("workspace")
        self.workspace.mkdir(exist_ok=True)

    def is_url(self, source: str) -> bool:
        return source.startswith("http://") or source.startswith("https://")

    def get_task_id(self, source: str) -> str:
        if self.is_url(source):
            return Path(urlparse(source).path).stem
        return Path(source).stem

    def load_from_url(self, url: str) -> Task:

        task_id = self.get_task_id(url)

        task_folder = self.workspace / task_id
        task_folder.mkdir(exist_ok=True)

        audio_path = task_folder / "original.wav"

        # Cache
        if audio_path.exists():

            task = Task(
                id=task_id,
                workspace=task_folder,
                audio=audio_path,
                cached=True
            )

            task.complete("loaded")

            return task

        print(f"[InputLoader] Downloading {task_id}...")

        try:

            with requests.get(url, stream=True) as response:

                response.raise_for_status()

                with open(audio_path, "wb") as f:

                    for chunk in response.iter_content(1024 * 1024):

                        if chunk:
                            f.write(chunk)

        except requests.RequestException as e:

            raise RuntimeError(f"Download failed: {e}")

        print("[InputLoader] Download completed.")

        task = Task(
            id=task_id,
            workspace=task_folder,
            audio=audio_path,
            cached=False
        )

        task.complete("loaded")

        return task

    def load_from_file(self, path: str) -> Task:

        src = Path(path)

        if not src.exists():
            raise FileNotFoundError(f"Audio file not found: {src}")

        task_id = self.get_task_id(path)

        task_folder = self.workspace / task_id
        task_folder.mkdir(exist_ok=True)

        audio_path = task_folder / "original.wav"

        # Cache
        if audio_path.exists():

            task = Task(
                id=task_id,
                workspace=task_folder,
                audio=audio_path,
                cached=True
            )

            task.complete("loaded")

            return task

        print(f"[InputLoader] Copying {src.name}...")

        shutil.copy2(src, audio_path)

        print("[InputLoader] Copy completed.")

        task = Task(
            id=task_id,
            workspace=task_folder,
            audio=audio_path,
            cached=False
        )

        task.complete("loaded")

        return task

    def load(self, source: str) -> Task:

        if self.is_url(source):
            return self.load_from_url(source)

        return self.load_from_file(source)