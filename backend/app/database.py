#to communicate with postgresql and FireBase

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings # for access to env vars(db config)

# db connection using postgres driver to use sql queries. No need if using sqlalchemy
while True:
    try:
        conn = psycopg2.connect(host=f'{settings.database_hostname}', database=f'{settings.database_name}', user=f'{settings.database_username}', password=f'{settings.database_password}', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connection successful!")
        break
    except Exception as e:
        print("DB connection failed:\n ", e)
        time.sleep(10)

# import os
# from dotenv import load_dotenv
# import firebase_admin
# from firebase_admin import credentials
# #from firebase_admin import auth, db

# load_dotenv() # Load from .env file
# cred = credentials.Certificate(os.getenv('FIREBASE_FILE_PATH'))

# # Initialize the Firebase Admin SDK
# firebase_admin.initialize_app(cred, {
#     'databaseURL' : 'https://auto-mark-grader-default-rtdb.firebaseio.com/',
#     'storageBucket': 'auto-mark-grader.appspot.com'
# })
