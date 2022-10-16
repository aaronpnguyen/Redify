from flask import Flask
from dotenv import load_dotenv
import os

if os.path.exists(".cache"):
    os.remove(".cache")

app = Flask(__name__)
app.secret_key = "Corbin/Aaron/Crawford/Nguyen/Redify/https://www.linkedin.com/in/aaronpnguyen/_/https://www.linkedin.com/in/corbin-crawford/"

DATABASE = 'redify'

load_dotenv()

SPOTIFY_APP_ID = os.getenv("APP_ID")
SPOTIFY_APP_SECRET = os.getenv("APP_SECRET")

'''
    Created by Aaron Nguyen and Corbin Crawford
    https://www.linkedin.com/in/aaronpnguyen/
    https://www.linkedin.com/in/corbin-crawford/
'''