from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse

from .. import schemas
#from ..database import get_db
from .. import generator

router = APIRouter(
    prefix="/upload",
    tags=['Upload'] # for documentation
)

@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate(textInput: schemas.TextInput):
        
    article = textInput.text
    # insert article into table

    # CLASSIFIER
    category = 'handball'

    # SUMMARIZER
    summary = article

    #vid gen
    generator.generate(summary, category)

    return {"video": "hehe"}


@router.get("/demo", status_code=status.HTTP_201_CREATED)
def demo():
    return FileResponse("reel.mp4", media_type="video/mp4")