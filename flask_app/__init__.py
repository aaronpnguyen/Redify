from flask import Flask
import os
app = Flask(__name__)
app.secret_key = "ohsnapthisisprettycrazyredifyiswild"

DATABASE = 'redify'

SPOTIFY_APP_ID = os.getenv("APP_ID")
SPOTIFY_APP_SECRET = os.getenv("APP_SECRET")