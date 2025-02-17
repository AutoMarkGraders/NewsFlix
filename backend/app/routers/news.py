from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse

from .. import schemas
from .. import summarizer
from .. import classifier
from .. import generator
from .. import extractor
import logging

router = APIRouter(
    prefix="/news",
    tags=['News'] # for documentation
)


@router.post("/image", status_code=status.HTTP_201_CREATED)
def image_to_text(image: UploadFile = File(...)):
    
    print("\nStarted!!!")

    # EXTRACTOR
    try:
        article = extractor.extract(image)
        print(f"\nARTICLE:\n{article}")

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")
    
    return JSONResponse(content={"text": article}, status_code=status.HTTP_200_OK)


@router.post("/text", status_code=status.HTTP_201_CREATED)
def text_to_reel(input_data: schemas.TextInput):
        
    print("\nStarted!!!")
    article = input_data.text
    targetLanguage = input_data.language
    # insert article into table

    # SUMMARIZER
    summary = summarizer.full_summarize(article)
    print(f"\nSUMMARY:\n{summary}")

    # CLASSIFIER
    category = classifier.full_classify(summary)
    print(f"\nCATEGORY:\n{category}")

    #vid gen
    generator.generate(summary, category, targetLanguage)

    return FileResponse("reel.mp4", media_type="video/mp4")


@router.get("/demo", status_code=status.HTTP_201_CREATED)
def demo(language: str):
    demo_reel = f'demo_{language}.mp4'
    return FileResponse(demo_reel, media_type="video/mp4")