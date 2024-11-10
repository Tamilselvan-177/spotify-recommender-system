import requests
import base64
import re
import numpy as np
import pandas as pd
from joblib import load

df = pd.read_csv("perfect_823.csv")
client_id = "34e60a3776424f988961869016476c91"
client_secret = "f99f254e50624134b73e4af94631c981"

# Step 1: Get Spotify access token
def get_access_token(client_id, client_secret):
    auth_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    payload = {
        "grant_type": "client_credentials"
    }
    response = requests.post(auth_url, headers=headers, data=payload)
    return response.json().get("access_token")

# Step 2: Get track details using Spotify API
def get_track_details(track_id, access_token):
    track_info_url = f"https://api.spotify.com/v1/tracks/{track_id}"
    response = requests.get(track_info_url, headers={"Authorization": f"Bearer {access_token}"})
    return response.json()

# Step 3: Preprocess the Release Date
def preprocess_release_date(release_date):
    return release_date.split('-')[0]  # Extract the year

# Main function to fetch track details, audio features, and predict the model
def collect_song_data(track_url):
    # Extract track ID from URL
    track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)

    # Get access token
    token = get_access_token(client_id, client_secret)

    # Fetch track details
    track_info = get_track_details(track_id, token)

    # Extract required fields
    track_name = track_info['name']
    artist_name = track_info['artists'][0]['name']
    track_duration = track_info['duration_ms'] / 1000  # Convert to seconds
    popularity = track_info['popularity']
    release_date = track_info['album']['release_date']

    # Preprocess Release Date to extract the year
    release_year = preprocess_release_date(release_date)

    # Placeholder for audio features
    audio_features = {
        'danceability': 0.7,  # Example value
        'acousticness': 0.1,  # Example value
        'energy': 0.8,        # Example value
        'liveness': 0.2,      # Example value
        'loudness': -5.0,     # Example value
        'speechiness': 0.05,  # Example value
        'tempo': 120          # Example value
    }

    # Prepare the data for prediction
    song_data = [
        track_duration,
        audio_features['danceability'],
        audio_features['acousticness'],
        audio_features['energy'],
        audio_features['liveness'],
        audio_features['loudness'],
        audio_features['speechiness'],
        audio_features['tempo'],
        popularity,
        int(release_year)  # Ensure it's an integer
    ]

    # Load the KNN model and make predictions
    loaded = load("knn_model.joblib")
    array = np.array(song_data).reshape(1, -1)
    index_data = loaded.kneighbors(array, n_neighbors=5)[1]  # Get indices of 5 nearest neighbors

    # Create a list of dictionaries for the results
    items = []
    for i in index_data[0]:  # index_data[0] gives the indices of the nearest neighbors
        name = df.iloc[i]['Track Name']
        url = df.iloc[i]['Track URL']
        items.append({"src": url, "text": name})
    print(items)
    return items  # Return the list of dictionaries


