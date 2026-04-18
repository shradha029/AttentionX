import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4

# Service imports (must be implemented by you)
from services.transcribe import transcribe_video
from services.highlight import get_highlights
from services.video_edit import cut_clips
from services.crop import crop_vertical
from services.captions import add_captions

app = FastAPI(title="AttentionX API")

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "../uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "../outputs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "AttentionX Backend Running 🚀"}


@app.post("/process-video")
async def process_video(file: UploadFile = File(...)):
    try:
        # Unique filename (avoid overwrite)
        unique_id = str(uuid4())
        file_ext = file.filename.split(".")[-1]
        filename = f"{unique_id}.{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # STEP 1: Transcription
        transcript = transcribe_video(file_path)

        # STEP 2: Highlight detection
        highlights = get_highlights(transcript)

        if not highlights:
            raise HTTPException(status_code=400, detail="No highlights found")

        # STEP 3: Clip extraction
        clip_paths = cut_clips(file_path, highlights, OUTPUT_DIR)

        final_videos = []

        # STEP 4 + 5: Crop + Captions
        for i, clip_info in enumerate(clip_paths):
            clip_path = clip_info["path"]
            hook = clip_info["hook"]

            # Vertical crop
            vertical_path = crop_vertical(clip_path)

            # Add captions + hook
            final_path = add_captions(vertical_path, hook)

            final_videos.append({
                "clip": final_path,
                "hook": hook
            })

        return JSONResponse({
            "status": "success",
            "total_clips": len(final_videos),
            "results": final_videos
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)