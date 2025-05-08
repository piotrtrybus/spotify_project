# spotify_oauth_app/oauth_utils.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

def get_auth_url():
    return (
        "https://accounts.spotify.com/authorize?"
        f"client_id={SPOTIFY_CLIENT_ID}&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}&scope=user-read-private user-read-email"
    )

def exchange_code_for_token(code):
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
    return response.json()

def get_user_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_url = "https://api.spotify.com/v1/me"
    profile_response = requests.get(profile_url, headers=headers)
    return profile_response.json()
