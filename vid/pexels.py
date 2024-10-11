import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('PEXELS_KEY')
url = 'https://api.pexels.com/v1/search'
headers = {
    'Authorization': API_KEY
}
params = {
    'query': 'disaster',  # search term
    'per_page': 3,  # Number of results 
    'orientation': 'landscape',
    #'color': 'green'
}

# download the images
response = requests.get(url, headers=headers, params=params).json()
for i, photo in enumerate(response['photos'], start=1):
    image_url = photo['src']['original']
    img_data = requests.get(image_url).content
    with open(f'{i}.jpg', 'wb') as handler:
        handler.write(img_data)    

print('Images downloaded successfully')