from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Task:
    # Basic Info
    id: str
    workspace: Path
    audio: Path

    # Loader
    cached: bool = False

    # Audio Info
    channels: int | None = None
    duration: float | None = None
    sample_rate: int | None = None

    # Generated Files
    speakers: list[Path] = field(default_factory=list)

    # Processing Results
    transcript: dict = field(default_factory=dict)
    timeline: dict = field(default_factory=dict)
    matches: list = field(default_factory=list)
    missing: list = field(default_factory=list)

    # Pipeline Status
    status: dict = field(default_factory=lambda: {
        "loaded": False,
        "split": False,
        "whisper": False,
        "timeline": False,
        "matched": False,
        "completed": False
    })

    # -------------------------
    # Helper Methods
    # -------------------------

    def complete(self, step: str):
        """Mark a pipeline step as completed."""
        if step not in self.status:
            raise ValueError(f"Unknown pipeline step: {step}")

        self.status[step] = True

        # لو كل الخطوات الأساسية خلصت
        if (
            self.status["loaded"]
            and self.status["split"]
            and self.status["whisper"]
            and self.status["timeline"]
            and self.status["matched"]
        ):
            self.status["completed"] = True

    def add_speaker(self, path: Path):
        """Add generated speaker audio."""
        self.speakers.append(path)

    def set_audio_info(self, channels: int, duration: float, sample_rate: int):
        """Store audio metadata."""
        self.channels = channels
        self.duration = duration
        self.sample_rate = sample_rate