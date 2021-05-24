# First group of settings for Data Retrieval

#Spotify developer app client id
client_id = ''
#Spotify developer app client secret
client_secret = ''

#------------Settings from here down are for Data Analysis-------------------

#Set to true if timezone needs to be adjusted
change_timezone=True
#the start and end of the range of dates to change timezone
timezone_change_start = '2020-03-22'
timezone_change_end = '2020-08-30'
#number of hours changes from UTC +0
hours_different = -8

#Set to True to remove songs and podcssts from first month for month analysis.
#For example if your first or last month only contains a couple of dats of data.
trim_first_month = True
trim_last_month = True


#Select columnss to correlate and visualize month to month.
song_attributes = ['Danceability','Energy','Acousticness', 'Valence',
                    'Mode', 'Instrumentalness']
#Reduced list of song attributes to visualize over months
song_attributes_2 = ['Instrumentalness','Energy']

# Third list of song attributes to visualize over months
song_attributes_3 = ['Danceability','Valence']


try:
    from private import *
except Exception:
    pass
