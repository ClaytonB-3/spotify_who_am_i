from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import ast
from os import listdir
import json
import settings

#client_id and client_secret set in settings.py
client_credentials_manager = SpotifyClientCredentials(client_id = settings.client_id,
                                client_secret = settings.client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def convert_json(path: str = 'MyData'):

    '''This function will return a list of dictionaries. Each dictionary will contain the trackName,
        trackArtist, end date and time it was listened to, and how many milliseconds of the track were listened to.
        How it does this is commented inline in the function''';

    '''Create a list of all file paths in the folder specified in the function parameter that start with the string
        'StreamingHistory', which is how Spotify delivers the listening history files.
        StreamingHistory0, StreamingHistory1, etc'''
    files = ['MyData/' + x for x in listdir(path) if x.split('.')[0][:-1] == 'StreamingHistory']
    # Read each json file into python, confirm it is a python object iwth ast.literal_eval, and add each
    # dictionary in the file to the end of a list and return the final list of dictionaries.
    all_streamings = []
    for file in files:
        with open(file, 'r', encoding = 'UTF-8') as f:
            new_streamings = ast.literal_eval(f.read())
            all_streamings += [streaming for streaming in new_streamings]
    return all_streamings

#Run the function on the file path where the listening histories are located (path entered in settings.py)
streaming_list = convert_json()

#convert list of dictionaries to a dataframe and then save as a csv
df_history = pd.DataFrame(streaming_list)
df_history.to_csv('full_streaming_history.csv')

'''For each dictionary in the full list of dictionaries of tracks,
check if the trackName is already in a new dictionary.
If it is not, add it with a value pair of the artistName.'''
track_artist_dict = {} #unique track artist pairs
for item in streaming_list:
    if item['trackName'] not in track_artist_dict:
        track_artist_dict[item['trackName']] = item['artistName']
#Print number of unique tracks
print('Number of unique tracks:',len(track_artist_dict))

''' Loop over the list of dictionaries and if the trackName is not in our
    count dictionary, add it and set value to one.
    If it is in the dictionary, increase the value by 1.'''
track_count_dict = {}
for item in streaming_list:
    if item['trackName'] in track_count_dict:
        track_count_dict[item['trackName']] += 1
    else:
        track_count_dict[item['trackName']] = 1

#Write functions to retrieve track info
def search_track_name(track_name: str, artist_name: str) -> str:

    '''This function takes the track name and artist name as parameters and combines them into a string and
       searches Spotify first for tracks, and then if there are no results, searches for podcasts that match
       the searched string. If there are no results for either it returns none. If a track or a podcast is
       found it returns the track id and the track type.

       In the sp.search function type refers to the type of Spotify item to search (e.g. track, episode, artist,
       album).  ''';

    search_track = sp.search(q=track_name+' '+artist_name, offset=0, type='track', market='US')
    if len(search_track['tracks']['items']) == 0:
        search_episode = sp.search(q=track_name+' '+artist_name, offset=0, type='episode',market = 'US')
        if search_episode['episodes']['items'] == [None]:
            return None, None
        else:
            try:
                track_id = search_episode['episodes']['items'][0]['id']
                track_type = search_episode['episodes']['items'][0]['type']
                return track_id, track_type
            except:
                print('search failed', track_name)
                return None, None
    else:
        track_id = search_track['tracks']['items'][0]['id']
        track_type = search_track['tracks']['items'][0]['type']
        return track_id, track_type

#Function to retrieve audio features
'''Note that only songs have audio features, podcasts do not.
  If we search an episode iD in this function it will return none'''

def get_features(track_id: str) -> dict:
    if track_id == None:
        return None
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except:
        return None

#Function to return track popularity from track id
def track_popularity(track_id: str):
    if track_id == None:
        return None
    try:
        track_info = sp.track(track_id)
        track_pop = track_info['popularity']
        return track_pop
    except:
        return None

'''Function to return artist genres, artist_id, artist popularity,
and artistName from track_id'''

def get_artist_info(track_id: str):
    if track_id == None:
        return None, None, None, None
    try:
        track_info = sp.track(track_id)
        artist_id = track_info['artists'][0]['id']
        artist_info = sp.artist(artist_id)
        artist_genres = artist_info['genres']
        artist_popularity = artist_info['popularity']
        artist_name = artist_info['name']
        return artist_id, artist_genres, artist_popularity, artist_name
    except:
        return None, None, None, None


'''Loop over dictionary of unique trackName:artistName pairs
   to retrieve all track and artist info'''

'''-----This loop can take a while to run, so testing on a
smaller dictionary can be a good use of time----'''
#Create dictionary that will house trackName:{trackFeature} key value pairs.
all_features = {}
#I included a list and counter to keep track of the loops progress as it takes a fair bit of time.
counter_list = [50, 100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800,1900,
                2000,2100,2200,2300,2400,2500,2600,2700,2800,2900,3000,3100,3200,3300,3400]
counter = 0
print('Start Loop')
for track, artist in track_artist_dict.items():
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    #Search for track and retrieve track id and track type (if search suceeeds)
    track_id, track_type = search_track_name(track, artist)
    #If the track_type is episode, create the track feature dictionary as no other functions work for podcasts
    if track_type == 'episode':
        additional_features = {'artist_name': artist, 'artist_genres': 'podcast', 'artist_popularity':None,
                               'track_popularity':None}
        all_features[track] = {'danceability': None, 'energy': None, 'key': None, 'loudness': None,
                               'mode': None, 'speechiness': None, 'acousticness': None, 'instrumentalness': None,
                               'liveness': None, 'valence': None, 'tempo': None, 'type': 'episode', 'id': track_id,
                               'uri': None, 'track_href': None, 'analysis_url': None, 'duration_ms': 0,
                               'time_signature': None}
        all_features[track].update(additional_features)

    #If the search did not find the track add an empty dictionary
    elif track_type == None:
        unknown_features = {'danceability': None, 'energy': None, 'key': None, 'loudness': None, 'mode': None,
                            'speechiness': None, 'acousticness': None, 'instrumentalness': None, 'liveness': None,
                            'valence': None, 'tempo': None, 'type': None, 'id': None, 'uri': None,
                            'track_href': None, 'analysis_url': None, 'duration_ms': 0, 'time_signature': None,
                            'artist_name': artist, 'artist_genres': None, 'artist_popularity':None,
                            'track_popularity':None}
        all_features[track] = unknown_features
    # If the track_type is track retrieve the track popularity, audio features, and artist info. Then fill out the
    # dictionary entry for the track with this information
    elif track_type == 'track':
        track_pop = track_popularity(track_id)
        artist_id, artist_genres, artist_popularity, artist_name = get_artist_info(track_id)
        additional_features = {'artist_name': artist, 'artist_genres': artist_genres, 'artist_popularity':artist_popularity, 'track_popularity':track_pop, 'type':'track'}
        features = get_features(track_id)
        if features:
            all_features[track] = features
            all_features[track].update(additional_features)
        else:  #In case there is a song with an id and without audio features.
            all_features[track] = {'danceability': None, 'energy': None, 'key': None, 'loudness': None, 'mode': None, 'speechiness': None, 'acousticness': None, 'instrumentalness': None, 'liveness': None, 'valence': None, 'tempo': None, 'type': 'Track', 'id': None, 'uri': None, 'track_href': None, 'analysis_url': None, 'duration_ms': 0, 'time_signature': None, 'artist_name': artist, 'artist_genres': None, 'artist_popularity':None, 'track_popularity':None}
            all_features[track].update(additional_features)

    #Optional progress tracking code
    counter += 1
    if counter in counter_list:
        print(counter,' done')
        print('length all features ',len(all_features))


print('IDs and Features retrieved')

#Create final list of tracks with attributes and save csv files
with_features = []
for track_name, features in all_features.items():
    #unpack the dictionary that was the value in `all_features` and concatinate it with the name of the track.
    with_features.append({'name': track_name, **features})

'''Create dataframe for saving to csv of track name and number of plays'''
track_names = []
for key in track_count_dict:
    track_names.append(key)
track_plays = []
for key in track_count_dict:
    track_plays.append(track_count_dict[key])
play_count_df = {'trackName':track_names,
                         'trackPlays':track_plays}

'''Save csv of all unique tracks with additional info
and csv of tracks with number of plays'''
df = pd.DataFrame(with_features)
df.to_csv('listening_history_unique_songs.csv')

df = pd.DataFrame(play_count_df)
df.to_csv('track_play_counts.csv')
