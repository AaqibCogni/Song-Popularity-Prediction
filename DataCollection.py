#!/usr/bin/env python
# coding: utf-8

# In[15]:


import lyricsgenius as lg
import numpy
from datetime import datetime
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import multiprocessing
from langdetect import detect_langs


# In[2]:


"""
Import the dataset.
We have used spotify dataset from Kaggle
link to the dataset:https://www.kaggle.com/datasets/yamaerenay/spotify-dataset-19212020-600k-tracks 
"""

tracks = pd.read_csv(r"D:\Study Material\Personal Projects\Song Popularity by Lyrics\tracks.csv")
print('Shape of the dataset:',tracks.shape)
tracks.head(5)


# In[3]:


tracks.info()


# In[42]:


"""Input : Dataframe with shape : 586672, 20
Purpose: 
1. remove the rows with missing values
2. Data cleaning of column Artist Name
3. Extracting Year from Release Date column
4. Filtering Songs with release year after 2020

Output: Filtered Dataframe with shape : 20218, 21 """

def clean_and_filter(df):
    print('Checking Missing Values in each feature',df.isnull().sum())
    # Drop the rows with null value in song name
    print('Dataset shape before dropping null values',df.shape)
    df.dropna(subset=['name'],inplace=True)
    print('Dataset shape after dropping null values',df.shape)
    df.reset_index(drop=True,inplace=True)
    
    # Artist name is given inside the list, unlist the values and save them as string
    df['artists'] = df['artists'].apply(lambda x : x.strip('[]'))
    df['artists'] = df['artists'].apply(lambda x : x.strip("''"))
    
    # Type Casy Release date to datetime datatype
    df['release_date'] = pd.to_datetime(df['release_date'])
    # Extract year from Released Date
    df['year'] = df['release_date'].dt.year
    
    # Getting Lyrics for 600k songs will be a time consuming task, therefore we will be taking a sample of 6k songs.
    # The sample taken consists of the songs released after 2020.
    tracks_sample = df.loc[df['year']>=2020]
    #tracks_sample =tracks.sample(n = 100)
    tracks_sample.reset_index(drop=True,inplace=True)
    print('SHape of sample dataset',tracks_sample.shape)
    return tracks_sample


# In[43]:


tracks_sample = clean_and_filter(tracks)


# In[44]:


# Check the distribution of popularity 
tracks_sample['popularity'].plot(kind = 'hist')
plt.show()


# In[ ]:


# Function without using multiprocessing. It takes 5 hours to extract lyrics for 20k songs.

"""
Function get_lyrics extracts lyrics of the songs present in all songs data based on Song Title and Artist Name
Parameter: all_songs dataframe
Return : all songs dataframe with lyrics
"""
token_name = 'KmchU-LsdwPv_5HCz7ghF7SjDd7BytiAvEGILwZCNuvgiqunYCDSRGNylQ56OkuR'
api = lg.Genius(token_name,sleep_time=0.01, verbose=False)

def get_lyrics(all_songs):
    all_song_data = pd.DataFrame()
    start_time = datetime.now()
    print("Started at {}".format(start_time))
    for i in range(0, len(all_songs)):
        song_title = all_songs.iloc[i]['name']
        song_title = re.sub(" and ", " & ", song_title)
        artist_name = all_songs.iloc[i]['artists']
        artist_name = re.sub(" and ", " & ", artist_name)
        try:
            song = api.search_song(song_title, artist=artist_name)
            song_lyrics = re.sub("\n", " ", song.lyrics)
        except:
            song_lyrics = "null"
        row = {
            "Song Title": all_songs.iloc[i]['name'],
            "Artist": all_songs.iloc[i]['artists'],
            "Lyrics": song_lyrics
        }
        all_song_data = all_song_data.append(row, ignore_index=True)
    end_time = datetime.now()
    print("\nCompleted at {}".format(start_time))
    print("Total time to collect: {}".format(end_time - start_time)) 
    return all_song_data
all_song_data = get_lyrics(tracks_sample)


# In[33]:


# Using Multiprocessing time taken to extract lyrics for 20k songs is reduced drastically from 5 hours to 35 minutes.

"""
Function get_lyrics extracts lyrics of the songs present in all songs data based on Song Title and Artist Name
Parameter: all_songs dataframe
Return : all songs dataframe with lyrics
"""
from multiprocessing import Pool

token_name = 'KmchU-LsdwPv_5HCz7ghF7SjDd7BytiAvEGILwZCNuvgiqunYCDSRGNylQ56OkuR'
api = lg.Genius(token_name,sleep_time=0.01, verbose=False,timeout=20)

def get_lyrics(all_songs):
    all_song_data = []
    start_time = datetime.now()
    print("Started at {}".format(start_time))
    query_list = []
    for i in range(0, len(all_songs)):
        song_title = all_songs.iloc[i]['name']
        song_title = re.sub(" and ", " & ", song_title)
        artist_name = all_songs.iloc[i]['artists']
        artist_name = re.sub(" and ", " & ", artist_name)
        query_list.append([song_title,artist_name]) 
    # Start one process per cpu core
    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        # More on starmap() below
        completed = p.starmap(api.search_song,query_list)
    all_song_data.append(completed)
        #all_song_data = all_song_data.append(row, ignore_index=True)
    end_time = datetime.now()
    print("\nCompleted at {}".format(start_time))
    print("Total time to collect: {}".format(end_time - start_time))
    return all_song_data
all_song_data = get_lyrics(tracks_sample)


# In[46]:


"""Input : List returned from get_lyrics function.
Purpose: 
1. Extract song title , artist and lyrics for each song present inside the list and store it inside a dataframe.
2. Attach popularity , duration and release year from the original tracks dataframe to the one created in above step.
3. Remove the songs where lyrics was not fetched
4. Detect an remove non english songs from the dataframe.

Output: Dataframe consisting of only English Songs with lyrics attached """

# Detect Non English Songs from the list of Songs
def get_eng_prob(text):
    detections = detect_langs(text)
    for detection in detections:
        if detection.lang == 'en':
            return detection.prob
    return 0

def data_prep(all_song_data):
    all_song_data_lyrics = pd.DataFrame()
    for i in range(0, len(all_song_data[0])):
        if all_song_data[0][i] == None:
            row = {
                "Song Title":'null',
                "Artist":'null',
                "Lyrics": 'null'
            }
            all_song_data_lyrics = all_song_data_lyrics.append(row, ignore_index=True)    
        if all_song_data[0][i]!= None:        
            row = {
                "Song Title": all_song_data[0][i].title,
                "Artist": all_song_data[0][i].artist,
                "Lyrics": all_song_data[0][i].lyrics
            }
            all_song_data_lyrics = all_song_data_lyrics.append(row, ignore_index=True)
            
            # Attach popularity, duration_ms, year to the all song dataset
            all_song_data_lyrics['Popularity'] = tracks_sample['popularity']
            all_song_data_lyrics['Duration_ms'] = tracks_sample['duration_ms']
            all_song_data_lyrics['Release Year'] = tracks_sample['year']

            # Remove the songs where Lyrics were not fetched
            all_song_data_final = all_song_data_lyrics.loc[all_song_data_lyrics['Lyrics']!='null']
            all_song_data_final.reset_index(drop=True,inplace=True)
            print('Shape of datset after removing songs with no lyrics fetched',all_song_data_final.shape)
            
            # Detect and remove non english songs
            all_song_data_final['en_prob'] = all_song_data_final['Lyrics'].map(get_eng_prob)
            print('Number of english songs: {}'.format(sum(all_song_data_final['en_prob'] >= 0.8)))
            print('Number of non-english songs: {}'.format(sum(all_song_data_final['en_prob'] < 0.8)))  
            all_song_data_final = all_song_data_final.loc[all_song_data_final['en_prob']>= 0.8]
            all_song_data_final.reset_index(drop=True,inplace=True)
            return all_song_data_final


# In[ ]:


all_song_data_final = data_prep(all_song_data)


# In[54]:


all_song_data_final.head(5)


# In[51]:


all_song_data_final['Lyrics'][1]


# In[53]:


all_song_data_final.to_excel(r'D:\Study Material\Personal Projects\Song Popularity by Lyrics\Song Popularity\ English Songs_with_Lyrics.xlsx',index=False)

