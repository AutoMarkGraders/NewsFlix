from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse

from .. import schemas
#from ..database import get_db
from .. import summarizer
from .. import classifier
from .. import generator
from .. import extractor
import logging

router = APIRouter(
    prefix="/news",
    tags=['News'] # for documentation
)

@router.post("/text", status_code=status.HTTP_201_CREATED)
def text_to_reel(textInput: schemas.TextInput):
        
    print("\nStarted!!!\n")
    article = textInput.text
    # insert article into table

    # SUMMARIZER
    summary = summarizer.full_summarize(article)
    print(f"\nSUMMARY:\n{summary}")

    # CLASSIFIER
    category = classifier.full_classify(summary)
    print(f"\nCATEGORY:\n{category}")

    #vid gen
    generator.generate(summary, category)

    return FileResponse("reel.mp4", media_type="video/mp4")


@router.post("/image", status_code=status.HTTP_201_CREATED)
def image_to_reel(image: UploadFile = File(...)):
    
    print("\nStarted!!!\n")

    # EXTRACTOR
    try:
        article = extractor.extract(image)
        print(f"\nARTICLE:\n{article}")

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    
    # SUMMARIZER
    summary = summarizer.full_summarize(article)
    print(f"\nSUMMARY:\n{summary}")

    # CLASSIFIER
    category = classifier.full_classify(summary)
    print(f"\nCATEGORY:\n{category}")

    #vid gen
    generator.generate(summary, category)

    return FileResponse("reel.mp4", media_type="video/mp4")


@router.get("/demo", status_code=status.HTTP_201_CREATED)
def demo():
    return FileResponse("reel.mp4", media_type="video/mp4")