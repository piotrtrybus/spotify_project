from flask import Flask
from spotify_oauth_app.app import app as spotify_oauth_blueprint
from os import load_dotenv

load_dotenv()

application = Flask(__name__)
application.secret_key = os.getenv('SPOTIFY_CLIENT_SECRET')
application.register_blueprint(spotify_oauth_blueprint)