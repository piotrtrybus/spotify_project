# /spotify-oauth-app/app.py
from flask import Blueprint, redirect, request, session, url_for
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Blueprint('spotify_oauth_app', __name__)

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Spotify login route
@app.route('/login')
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize?"
        f"client_id={SPOTIFY_CLIENT_ID}&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}&scope=user-read-private user-read-email"
    )
    return redirect(auth_url)

# Callback route after Spotify redirects
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Error: No code received", 400

    # Exchange code for access token
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {requests.auth._basic_auth_str(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)}"
    }
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
    }
    response = requests.post(token_url, data=data, headers=headers)
    response_data = response.json()

    if "access_token" in response_data:
        session['access_token'] = response_data['access_token']
        return redirect(url_for('spotify_oauth_app.profile'))
    else:
        return "Error: Unable to retrieve access token", 400

# Profile route to get user info
@app.route('/profile')
def profile():
    if 'access_token' not in session:
        return redirect(url_for('spotify_oauth_app.login'))

    access_token = session['access_token']
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    profile_url = "https://api.spotify.com/v1/me"
    profile_response = requests.get(profile_url, headers=headers)
    profile_data = profile_response.json()

    return profile_data
