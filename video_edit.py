from moviepy import VideoFileClip
import os


def cut_clips(video_path: str, highlights: list, output_dir: str):
    """
    Input:
        video_path → original video
        highlights → [{start, end, hook}]
        output_dir → where clips will be saved

    Output:
        [
          {"path": "clip_0.mp4", "hook": "..."}
        ]
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError("Video file not found")

    os.makedirs(output_dir, exist_ok=True)

    video = VideoFileClip(video_path)
    clips_output = []

    for i, h in enumerate(highlights):
        start = int(h["start"])
        end = int(h["end"])
        hook = h["hook"]

        # Safety check
        if start >= end or end > video.duration:
            continue

        clip = video.subclip(start, end)

        output_path = os.path.join(output_dir, f"clip_{i}.mp4")

        clip.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac"
        )

        clips_output.append({
            "path": output_path,
            "hook": hook
        })

    video.close()

    return clips_output