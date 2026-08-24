from fastapi import (
    FastAPI,
    Form,
    UploadFile,
    File
)

from fastapi.responses import StreamingResponse

from model import ImageGenerator

from PIL import Image

import io


app = FastAPI(
    title="AI Image & Text API",
    version="1.0"
)


# ==========================================
# LOAD MODELS
# ==========================================

generator = ImageGenerator()


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "status": "running",

        "models": {
            "text_to_image":
                "segmind/tiny-sd",

            "image_to_text":
                "Salesforce/blip-image-captioning-base"
        },

        "endpoints": {
            "generate_image":
                "/generate",

            "generate_text":
                "/image-to-text"
        }
    }


# ==========================================
# TEXT → IMAGE
# ==========================================

@app.post("/generate")
async def generate_image(
    prompt: str = Form(...)
):

    try:

        image = generator.generate_image(
            prompt
        )

        buffer = io.BytesIO()

        image.save(
            buffer,
            format="PNG"
        )

        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="image/png"
        )

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ==========================================
# IMAGE → TEXT
# ==========================================

@app.post("/image-to-text")
async def image_to_text(
    file: UploadFile = File(...)
):

    try:

        # Read image

        image_data = await file.read()

        image = Image.open(
            io.BytesIO(image_data)
        ).convert("RGB")

        # Generate text

        text = generator.generate_text(
            image
        )

        return {
            "success": True,
            "filename": file.filename,
            "generated_text": text
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }