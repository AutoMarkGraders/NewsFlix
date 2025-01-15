from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse

from .. import schemas
#from ..database import get_db
from .. import generator

router = APIRouter(
    prefix="/news",
    tags=['News'] # for documentation
)

@router.post("/text", status_code=status.HTTP_201_CREATED)
def generate(textInput: schemas.TextInput):
        
    article = textInput.text
    # insert article into table

    # CLASSIFIER
    category = 'handball'

    # SUMMARIZER
    summary = article

    #vid gen
    generator.generate(summary, category)

    return FileResponse("reel.mp4", media_type="video/mp4")


@router.post("/image", status_code=status.HTTP_201_CREATED)
def ocr_image(image: UploadFile = File(...)):
    
    # save image
    
    # article = ocr(image)

    # CLASSIFIER

    # SUMMARIZER

    #vid gen
    #generator.generate(summary, category)

    return FileResponse("reel.mp4", media_type="video/mp4")


@router.get("/demo", status_code=status.HTTP_201_CREATED)
def demo():
    return FileResponse("reel.mp4", media_type="video/mp4")