import json
import subprocess
from pathlib import Path


class FFmpegUtils:

    @staticmethod
    def probe_audio(audio_path: Path) -> dict:

        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_streams",
            str(audio_path)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        data = json.loads(result.stdout)

        if "streams" not in data or len(data["streams"]) == 0:
            raise RuntimeError("No audio streams found.")

        stream = data["streams"][0]

        return {

            "channels": stream.get("channels"),

            "sample_rate": int(stream.get("sample_rate")),

            "duration": float(stream.get("duration")),

            "bit_rate": int(stream.get("bit_rate", 0)),

            "codec": stream.get("codec_name")

        }