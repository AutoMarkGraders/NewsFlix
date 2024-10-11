#functions to write to table

from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, insert, select, update, func

from .. import schemas
#from ..database import get_db
from .. import generator
import datetime
import os
from dotenv import load_dotenv
import requests
from math import ceil
from random import randrange

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

    n = article.count(' ') + 1 # no.of words
    print(f'Number of words: {n}')

    # download the images
    load_dotenv()
    API_KEY = os.getenv('PEXELS_KEY')
    url = 'https://api.pexels.com/v1/search'
    headers = {
        'Authorization': API_KEY
    }
    params = {
        'query': f'{category}',  # search term
        'per_page': ceil(n/25),  # Number of results 
        'orientation': 'landscape',
    }
    response = requests.get(url, headers=headers, params=params).json()
    for i, photo in enumerate(response['photos'], start=1):
        image_url = photo['src']['original']
        img_data = requests.get(image_url).content
        with open(f'{i}.jpg', 'wb') as handler: # saved in CWD (backend/)
            handler.write(img_data)    

    # SUMMARIZER
    summary = article

    #vid gen
    generator.generate(summary, n)

    return {"video": "hehe"}


