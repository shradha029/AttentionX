from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import os
def add_captions(video_path: str, hook: str):
    """
    Adds:
    - Hook (top)
    - Simple caption (bottom)
    """

    if not os.path.exists(video_path):
        raise FileNotFoundError("Video not found")

    video = VideoFileClip(video_path)

    
    hook_text = TextClip(
        hook.upper(),
        fontsize=70,
        color='white',
        bg_color='black',
        size=(video.w, None),
        method='caption'
    ).set_position(("center", "top")).set_duration(3)

    # 🎯 SIMPLE CAPTION (Bottom)
    caption_text = TextClip(
        "Stay focused. Stay consistent.",
        fontsize=50,
        color='white',
        bg_color='black',
        size=(video.w, None),
        method='caption'
    ).set_position(("center", "bottom")).set_duration(video.duration)

    final = CompositeVideoClip([video, hook_text, caption_text])

    output_path = video_path.replace(".mp4", "_final.mp4")

    final.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    video.close()

    return output_path