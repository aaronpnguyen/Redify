from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = "ohsnapthisisprettycrazyredifyiswild"

DATABASE = 'redify'

load_dotenv()

SPOTIFY_APP_ID = os.getenv("APP_ID")
SPOTIFY_APP_SECRET = os.getenv("APP_SECRET")