import os
from flask import Flask, Blueprint, redirect, request, session, url_for
from .oauth_utils import get_auth_url, exchange_code_for_token, get_user_profile

spotify_oauth_blueprint = Blueprint('spotify_oauth_app', __name__)

@spotify_oauth_blueprint.route('/login')
def login():
    return redirect(get_auth_url())

@spotify_oauth_blueprint.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code received", 400

    token_data = exchange_code_for_token(code)
    if "access_token" in token_data:
        session['access_token'] = token_data['access_token']
        return redirect(url_for('spotify_oauth_app.profile'))
    return "Error: Unable to retrieve access token", 400

@spotify_oauth_blueprint.route('/profile')
def profile():
    if 'access_token' not in session:
        return redirect(url_for('spotify_oauth_app.login'))

    profile_data = get_user_profile(session['access_token'])
    return profile_data

@spotify_oauth_blueprint.route('/')
def index():
    return 'Spotify OAuth app is running.'

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key")
app.register_blueprint(spotify_oauth_blueprint)
