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
    'query': 'forest',  # search term
    'per_page': 1,  # Number of results 
    'orientation': 'landscape',
    #'color': 'green'
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
image_url = data['photos'][0]['src']['original'] 

# download the image
img_data = requests.get(image_url).content
with open('stock_image.jpg', 'wb') as handler:
    handler.write(img_data)

print('Image downloaded successfully')