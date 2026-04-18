import cv2
import mediapipe as mp
from moviepy import VideoFileClip
import os


mp_face = mp.solutions.face_detection.FaceDetection(model_selection=0)


def get_face_center(frame):
    results = mp_face.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.detections:
        bbox = results.detections[0].location_data.relative_bounding_box
        h, w, _ = frame.shape

        x = int((bbox.xmin + bbox.width / 2) * w)
        y = int((bbox.ymin + bbox.height / 2) * h)

        return x, y

    return None


def crop_vertical(video_path: str):
    if not os.path.exists(video_path):
        raise FileNotFoundError("Clip not found")

    video = VideoFileClip(video_path)

    # Get first frame
    frame = video.get_frame(0)

    face_center = get_face_center(frame)

    w, h = video.size

    # Target vertical width (9:16)
    new_w = int(h * 9 / 16)

    if face_center:
        cx, _ = face_center
    else:
        cx = w // 2  # fallback center

    x1 = max(0, cx - new_w // 2)
    x2 = min(w, cx + new_w // 2)

    cropped = video.crop(x1=x1, x2=x2)

    output_path = video_path.replace(".mp4", "_vertical.mp4")

    cropped.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    video.close()

    return output_path