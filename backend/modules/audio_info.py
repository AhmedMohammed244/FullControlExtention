from models.task import Task

from utils.ffmpeg_utils import FFmpegUtils


class AudioInfo:

    def analyze(self, task: Task) -> Task:

        info = FFmpegUtils.probe_audio(task.audio)

        task.set_audio_info(

            channels=info["channels"],

            duration=info["duration"],

            sample_rate=info["sample_rate"],
            
            bit_rate=info["bit_rate"],
            
            codec=info["codec"]

        )

        task.complete("audio_info")

        return task