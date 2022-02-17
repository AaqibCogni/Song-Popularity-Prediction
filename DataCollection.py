#!/usr/bin/env python
# coding: utf-8
import lyricsgenius as lg
import billboard
import numpy
from datetime import datetime
import pandas as pd
# from gc import is_finalized
from pprint import pprint
from sre_constants import BRANCH
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.client import SpotifyException
from textdistance import cosine
import warnings
warnings.filterwarnings("ignore")

"""
Function collect_hot100_from_billboard collects the Top 100 songs from billboard platform from a Data range passed to it as parameters.
Parameters: 
1. start_year
2. end_year

Returns a Dataframe with Song Title, Artist and Year of the song.
"""
def collect_hot100_from_billboard(start_year,end_year):
    years = np.arange(start_year,end_year + 1)
    dataset = pd.DataFrame()
    for i in years:
        date = str(i) + '-' + '01' + '-' + '01'
        chart = billboard.ChartData('hot-100', date = date)
        for j in range(0,100):
            row = { 
                'Song Title': chart.entries[j].title,
                'Artist':chart.entries[j].artist,
                'Year': i
            }
            dataset = dataset.append(row, ignore_index=True)
    return dataset
all_songs = collect_hot100_from_billboard(2000,2020)

"""
Function get_lyrics extracts lyrics of the songs present in all songs data based on Song Title and Artist Name
Parameter: all_songs dataframe
Return : all songs dataframe with lyrics
"""

api = lg.Genius(token_name,sleep_time=0.01, verbose=False)

def get_lyrics(all_songs):
    all_song_data = pd.DataFrame()
    start_time = datetime.now()
    print("Started at {}".format(start_time))
    for i in range(0, len(all_songs)):
        song_title = all_songs.iloc[i]['Song Title']
        song_title = re.sub(" and ", " & ", song_title)
        artist_name = all_songs.iloc[i]['Artist']
        artist_name = re.sub(" and ", " & ", artist_name)
        try:
            song = api.search_song(song_title, artist=artist_name)
            song_lyrics = re.sub("\n", " ", song.lyrics)
        except:
            song_lyrics = "null"
        row = {
            "Year": all_songs.iloc[i]['Year'],
            "Song Title": all_songs.iloc[i]['Song Title'],
            "Artist": all_songs.iloc[i]['Artist'],
            "Lyrics": song_lyrics
        }
        all_song_data = all_song_data.append(row, ignore_index=True)
    end_time = datetime.now()
    print("\nCompleted at {}".format(start_time))
    print("Total time to collect: {}".format(end_time - start_time)) 
    return all_song_data
all_song_data = get_lyrics(all_songs)

"""
Function to get the popularity score of the songs from spotify based on track and artist

"""
API_MAX_OFFSET = 150
API_MAX_LIMIT = 50
auth_manager = SpotifyClientCredentials(client_id,
                                       client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)
def is_similar(A, B, rate=0.75):
    a = A.lower()
    b = B.lower()
    similarity = cosine.normalized_similarity(a, b)
    if similarity >= rate:
        return True
    return False

def get_popularity(track, artist):
    offset = -1
    max_popularity = 0
    
    while True:

        if offset == API_MAX_OFFSET:
            break
        try:
            offset = 0 if offset == -1 else offset
            results = sp.search(q=f"track:{track}", type='track', limit=50, offset=offset)
        except SpotifyException as e:
            break
        items = results['tracks']['items']    
        size = len(items)
        if size == 0:
            break
        offset += size   
        for item in items:
            uri = item["uri"]
            name = item["name"]
            album = item["album"]["name"]
            popularity = item["popularity"]

            artists = [a["name"] for a in item["artists"] if is_similar(a["name"], artist)]
            if not artists:
                continue
            # if not is_similar(track, name):
            #     continue
            # else:
            #     print(uri, album, name, artists, popularity)

            if popularity > max_popularity:
                max_popularity = popularity
        if offset < API_MAX_LIMIT:
            break
    return max_popularity

if __name__ == "__main__":
    all_song_data['Popularity'] = ''
    for i in all_song_data.index:
        track = all_song_data['Song Title'][i]
        artist = all_song_data['Artist'][i]
        all_song_data['Popularity'][i] = get_popularity(track, artist)

all_song_data.to_excel(r'D\....\all_song_data_with_popularity',index=False)

