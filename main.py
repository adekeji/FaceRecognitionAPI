from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import numpy as np
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import logging

app = FastAPI(
    title="Face Recognition API",
    description="API for face recognition operations",
    version="1.0.0"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Face Recognition API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/detect-faces")
async def detect_faces(image: UploadFile = File(...)):
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image type. Only JPEG and PNG are supported.")

    contents = await image.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 5MB.")

    try:
        pil_image = Image.open(BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="Cannot identify image file.")

    image_array = np.array(pil_image)
    face_locations = face_recognition.face_locations(image_array)

    faces = [{"top": top, "right": right, "bottom": bottom, "left": left} 
             for (top, right, bottom, left) in face_locations]

    response = {
        "faces": faces,
        "count": len(face_locations),
        "message": "Faces detected successfully." if faces else "No faces detected."
    }

    return JSONResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)