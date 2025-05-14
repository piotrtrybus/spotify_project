import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get sensitive data from environment variables
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')

# Generate the authorization URL for Spotify OAuth
def get_auth_url():
    return (
        "https://accounts.spotify.com/authorize?"
        f"client_id={SPOTIFY_CLIENT_ID}&response_type=code"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope=user-read-private"
    )

# Exchange the authorization code for an access token
def exchange_code_for_token(code):
    token_url = "https://accounts.spotify.com/api/token"
    auth = HTTPBasicAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
    }
    response = requests.post(token_url, data=data, auth=auth)

    if response.status_code == 200:
        return response.json()  
    else:
        return {"error": "Unable to exchange code for token", "status_code": response.status_code, "details": response.text}

# Fetch the user profile using the access token
def get_user_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_url = "https://api.spotify.com/v1/me"
    profile_response = requests.get(profile_url, headers=headers)

    if profile_response.status_code == 200:
        return profile_response.json()  
    else:
        return {"error": "Unable to fetch user profile", "status_code": profile_response.status_code, "details": profile_response.text}
