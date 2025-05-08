import requests

def get_current_playing_track(access_token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 204:
        return {"message": "Nothing is currently playing"}
    return response.json()


response = get_current_playing_track(access_token)
print(response)