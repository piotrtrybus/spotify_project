import requests
import sys
import os

# Add the parent directory of the current file to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from spotify_oauth_app.oauth_utils import get_user_profile, get_access_token,get_auth_url

access_token = get_access_token()

def get_current_playing_track(access_token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 204:
        return {"message": "Nothing is currently playing"}
    return response.json()


