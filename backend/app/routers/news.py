from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
import logging
import requests

from .. import schemas
from .. import extractor
from .. import nlp
from .. import generator

router = APIRouter(
    prefix="/news",
    tags=['News'] # for documentation
)


@router.post("/image", status_code=status.HTTP_201_CREATED)
def image_to_text(image: UploadFile = File(...)):
    
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

    # SUMMARIZER
    summary = nlp.full_summarize(article)
    print(f"\nSUMMARY:\n{summary}")

    # CLASSIFIER
    category = nlp.full_classify(summary)
    print(f"\nCATEGORY:\n{category}")

    #vid gen
    generator.generate(summary, category, targetLanguage)

    # upload to cloudinary
    data = {'upload_preset': 'upload_reels'}
    files = {'file': open('outputs/reel.mp4', 'rb')}
    response = requests.post('https://api.cloudinary.com/v1_1/news-to-reel/video/upload', data=data, files=files)
    reel_url = response.json()['secure_url']
    print(reel_url)

    # insert data into table

    return JSONResponse(content={"reel_url": reel_url}, status_code=status.HTTP_200_OK)

    # return FileResponse("outputs/reel.mp4", media_type="video/mp4")


@router.get("/demo", status_code=status.HTTP_201_CREATED)
def demo(language: str):
    demo_reel = f'outputs/demo_{language}.mp4'
    return FileResponse(demo_reel, media_type="video/mp4")