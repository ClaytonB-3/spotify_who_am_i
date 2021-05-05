import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from datetime import datetime, timedelta, time
import matplotlib.style as style
import settings
style.use(style='fivethirtyeight')

#Read in csv with all info for all unique tracks in my listening history
df = pd.read_csv('listening_history_unique_songs.csv')
#Read in csv to dataframe full listening history
df_full_history = pd.read_csv('full_streaming_history.csv')

print('Listening History Columns:', df.columns)
print('Unique songs with additional attributes columns:', df_full_history.columns)

#Update column titles to match across dataframes where appropriate
name_mapper = {'name':'trackName'}
df.rename(columns=name_mapper, inplace=True)
artist_mapper = {'artist_name':'artistName'}
df.rename(columns=artist_mapper, inplace=True)
type_mapper = {'type':'Type'}
df.rename(columns=type_mapper, inplace=True)
#Capitalize attribute columns
att_mapper = {'danceability':'Danceability', 'energy':'Energy', 'key':'Key', 'loudness':'Loudness',
       'mode':'Mode', 'speechiness':'Speechiness', 'acousticness':'Acousticness',
        'instrumentalness':'Instrumentalness', 'liveness':'Liveness', 'valence':'Valence', 'tempo':'Tempo'}
df.rename(columns=att_mapper, inplace=True)
print(df.columns)
print(df_full_history.columns)

#Merge dataframes on trackName and artistName
df_full_hist_atr = df_full_history.merge(right=df, how='left', on=['trackName','artistName'])

#create datetime object from the endTime and remove the previous endTime column
df_full_hist_atr['endTime_dt'] = pd.to_datetime(df_full_hist_atr['endTime'])
df_full_hist_atr.drop('endTime', inplace=True, axis=1)

#drop unnecessary columns
df_full_hist_atr.drop('Unnamed: 0_x', inplace=True, axis=1)
df_full_hist_atr.drop('uri', inplace=True, axis=1)
df_full_hist_atr.drop('track_href', inplace=True, axis=1)
df_full_hist_atr.drop('analysis_url', inplace=True, axis=1)
df_full_hist_atr.drop('Unnamed: 0_y', inplace=True, axis=1)

'''Update the endTime column to your timezone. Settings are in settings.py to be configured.
Code allows for a beginning and end of time to change along with the time difference.''';
if settings.change_timezone:
        df_full_hist_atr.loc[(df_full_hist_atr.endTime_dt > settings.timezone_change_start)
                             &(df_full_hist_atr.endTime_dt < settings.timezone_change_end),
                              'endTime_dt'] = df_full_hist_atr.endTime_dt + timedelta(hours=settings.hours_different)

#Visualize missing data
plt.figure(figsize=(12,6))
heat_map = sns.heatmap(df_full_hist_atr.isnull(), cbar=False)
heat_map.set_yticklabels([])
plt.show()

'''If the id is null the search function from the data retrieval step was
unable to find the track. Here we print the number of
tracks that were not found.'''
print(len(df_full_hist_atr[df_full_hist_atr['id'].isna()][['Type','trackName','artist_genres','Danceability','id']]),'Tracks were not found and have all null values.')

'''Creating a new dataframe that contains rows from the previous full dataframe with rows with a
null value in the 'id' column meaning the search in the data retrieval was unable to find them'''

clean_full_df = df_full_hist_atr[df_full_hist_atr['id'].notna()].copy()

#Add column converting msPlayed to minutes played
def ms_to_min(col):
    col_float = float(col)
    return col_float/60000

clean_full_df['Minutes_Played'] = clean_full_df['msPlayed'].apply(ms_to_min)

'''In order to group songs and podcasts by when they were listened to we'll write functions
to extract the month and year, day of the week, and time of day, from the endTime datetime object.'''

def extract_month_year(col): #Function to return year/month from datetime object
        return datetime.strftime(col, '%Y/%m')

def extract_day_of_week(col): #Function to return day of week from datetime object
        return str(datetime.strftime(col, '%w'))

def time_of_day(col): #Function to return time of day from datetime object
        if datetime.strftime(col, '%H.%M') > '00' and datetime.strftime(col, '%H.%M') <= '04':
            return '0-4'
        if datetime.strftime(col, '%H.%M') > '04' and datetime.strftime(col, '%H.%M') <= '08':
            return '4-8'
        if datetime.strftime(col, '%H.%M') > '08' and datetime.strftime(col, '%H.%M') <= '12':
            return '8-12'
        if datetime.strftime(col, '%H.%M') > '12' and datetime.strftime(col, '%H.%M') <= '16':
            return '12-16'
        if datetime.strftime(col, '%H.%M') > '16' and datetime.strftime(col, '%H.%M') <= '20':
            return '16-20'
        if datetime.strftime(col, '%H.%M') > '20' and datetime.strftime(col, '%H.%M') <= '24':
            return '20-24'

#Create new columns in the dataframe for the month/year the track was listened to in and the day of the week
clean_full_df['month_year'] = clean_full_df['endTime_dt'].apply(extract_month_year)
clean_full_df['day_of_week'] = clean_full_df['endTime_dt'].apply(extract_day_of_week)
clean_full_df['Time of Day'] = clean_full_df['endTime_dt'].apply(time_of_day)

#Checking number of tracks in first and last month.
print('Number of tracks in first month: ', len(clean_full_df['month_year'].min()))
print('Number of tracks in last month: ', len(clean_full_df['month_year'].max()))

'''Here we are creating a new trimmed data frame without the first and last month of data
as those may be shorter months. We're using the month_year column we just created
to remove the first and last month. Set trim_first_month and trim_last_month appropriately
in settings.py for your data if you want to trim them.'''
if settings.trim_first_month and settings.trim_last_month:
        trimmed_full_df = (clean_full_df[(clean_full_df['month_year'] != clean_full_df['month_year'].min())
                        & (clean_full_df['month_year'] != clean_full_df['month_year'].max())].copy())

elif settings.trim_first_month and not settings.trim_last_month:
        trimmed_full_df = clean_full_df[(clean_full_df['month_year'] != clean_full_df['month_year'].min())].copy()

elif settings.trim_last_month and not settings.trim_first_month:
        trimmed_full_df = clean_full_df[(clean_full_df['month_year'] != clean_full_df['month_year'].max())].copy()

elif not settings.trim_last_month and not settings.trim_first_month:
        trimmed_full_df = clean_full_df.copy()

#Note that even if you do not need to trim your data the df will be called trimmed

'''In the spirit of Spotify's Year in Review, a summary of your years Spotify use,
and a service I love, I calculated a few basic summary statistics. '''

songs = clean_full_df[clean_full_df['Type'] == 'track'].copy()
podcasts = clean_full_df[clean_full_df['Type'] == 'episode'].copy()
print('Over the last 12 months you listened to:', round(sum(songs['Minutes_Played']),2), 'minutes of music.')
print('Over the last 12 months you listened to:', round(sum(podcasts['Minutes_Played']),2), 'minutes of podcasts.')
print('For a total of:',round(sum(clean_full_df['Minutes_Played']),2), 'minutes of Spotify audio content.')
print('You listened to', songs['artistName'].nunique(), 'unique musical artists on Spotify with an average popularity weighted by plays of',round(songs['artist_popularity'].mean(),2))
print('for a total of', len(songs), 'songs.', songs['trackName'].nunique(), 'of which were unique songs with an average popularity weighted by plays of',round(songs['track_popularity'].mean(),2))
print('Moving on to podcasts you listened to',podcasts['artistName'].nunique(),'different podcasts.')
print('and a total of',len(podcasts),'episodes.')

'''Moving on to analyzing and visualizing listening patterns'''
#Create dataframe of just songs (removing the podcasts) to vizualize song attributes over time
all_song_plays_trim = trimmed_full_df[trimmed_full_df['Type']=='track']
print('There are',len(all_song_plays_trim),'songs in the final songs only trimmed dataframe.')

'''Calculate correlations between all of the attributes we are looking at
(Danceability, Energy, Acousticness, Valence, Mode, and Instrumentalness).
The list of attributes analyzed can be changed in settings.py'''
all_song_features_corr = all_song_plays_trim[settings.song_attributes].corr()

#Plot the correlations
fig, ax = plt.subplots(figsize=(12,10))
att_heatmap = sns.heatmap(all_song_features_corr)
plt.title("Song Attribute Correlations", fontsize=24, fontweight=750, pad=15)
plt.yticks(rotation = 45, fontsize = 14)
plt.xticks(rotation = 45, fontsize = 14)

plt.show()

'''Time to visualize the attribute on a month basis. Start by grouping the
all songs dataframe by the month_year column and take the mean of each
attribute for each month. Then sort the values by the month/year'''
month_avg = (all_song_plays_trim[settings.song_attributes + ['month_year']]
             .groupby('month_year').mean().sort_values(by='month_year').reset_index())

'''Melt the data frame on the month_year column.
This will leave us with the attribute:average pair for each month/year'''
melt_attribute_avg_month = month_avg.melt(id_vars='month_year')
var_mapper = {'variable':'Variable'}
melt_attribute_avg_month.rename(columns=var_mapper, inplace=True)

'''Plot all selected attributes monthly average over the course of time'''
#x-axis labels and locations for months
xlabels = ['May 2020', 'June 2020', 'July 2020', 'August 2020', 'September 2020', 'October 2020', 'November 2020', 'December 2020', 'January 2021', 'February 2021', 'March 2021', 'April 2021']
label_loc = np.arange(len(xlabels))

fig, ax = plt.subplots(figsize=(20, 12)) #Create figure and subplot
sns.lineplot(x='month_year', y='value', hue='Variable', data=melt_attribute_avg_month) #create lineplot
#Plot Title
plt.title("Music Tendencies by Month", fontsize=28, fontweight=750, pad=20)
#Legend settings
plt.setp(ax.get_legend().get_texts(), fontsize='22')
plt.setp(ax.get_legend().get_title(), fontsize='32')
plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0, fontsize=18,
           title = 'Attribute', title_fontsize=22, labelspacing=0.6)
#Axis ticks and labels
plt.ylabel('Value', fontsize=26, labelpad=10)
ax.set_xticks(label_loc)
ax.set_xticklabels(labels = xlabels, rotation = 75, fontsize=20)
plt.yticks(rotation = 45, fontsize=18)
plt.grid(b=False, which='both',axis='y')
ax.set(xlabel=None)
#Remove horizontal grid lines
plt.grid(b=False, which='both',axis='y')


plt.show()

'''Plot just energy and acousticness and danceability and valence together.
These additional graph attribute selections can be changed in settings.py'''

'''Create a new dataframe with just the rows of the attributes we want to isolate.
These variables can be changed in the settings.py file.'''
melt_attribute_trim = melt_attribute_avg_month[melt_attribute_avg_month['Variable'].str.contains(
                        '|'.join(settings.song_attributes_2)).any(level=0)]
#Create figure, axes, and lineplot
fig, ax = plt.subplots(figsize=(20, 12))
sns.lineplot(x='month_year', y='value', hue='Variable', data=melt_attribute_trim, palette = 'dark')
#Plot title
plt.title("Energy and Accousticness by Month", fontsize=28, fontweight=750, pad = 20)
#Legend settings
plt.setp(ax.get_legend().get_texts(), fontsize='22')
plt.setp(ax.get_legend().get_title(), fontsize='32')
#Axis ticks and labels
plt.ylabel('Value', fontsize=26, labelpad=10)
ax.set_xticks(label_loc)
ax.set_xticklabels(labels = xlabels, rotation = 75, fontsize=20)
plt.yticks(rotation = 45, fontsize=18)
plt.grid(b=False, which='both',axis='y')
ax.set(xlabel=None)
#Remove horizontal grid lines
plt.grid(b=False, which='both',axis='y')


plt.show()

#Focused attribute over time plot number 2
'''Create a new dataframe with just the rows of the attributes we want to isolate.
These variables can be changed in the settings.py file.'''
melt_attribute_trim2 = melt_attribute_avg_month[melt_attribute_avg_month['Variable'].str.contains(
                        '|'.join(settings.song_attributes_3)).any(level=0)]

#Create figure, axes, and lineplot
fig, ax = plt.subplots(figsize=(20, 12))
sns.lineplot(x='month_year', y='value', hue='Variable', data=melt_attribute_trim2, palette = 'pastel')
#Plot title
plt.title("Danceability and Valence by Month", fontsize=28, fontweight=750, pad = 20)
#Legend settings
plt.setp(ax.get_legend().get_texts(), fontsize='22')
plt.setp(ax.get_legend().get_title(), fontsize='32')
#Axis ticks and labels
plt.ylabel('Value', fontsize=26, labelpad=10)
ax.set_xticks(label_loc)
ax.set_xticklabels(labels = xlabels, rotation = 75, fontsize=20)
plt.yticks(rotation = 45, fontsize=18)
plt.grid(b=False, which='both',axis='y')
ax.set(xlabel=None)
#Remove horizontal grid lines
plt.grid(b=False, which='both',axis='y')


plt.show()

'''Visualize total minutes listened to month by month comparing
songs to podcasts. Group by type and year and sum the minutes players.
We'll also change episode to Podcast and track to Song in the type
column for clarity.'''
month_count_all = (trimmed_full_df[['Type','month_year', 'Minutes_Played']]
                   .groupby(['Type','month_year']).sum().reset_index().sort_values('month_year'))
month_count_all.loc[month_count_all.Type == 'episode', 'Type'] = 'Podcast'
month_count_all.loc[month_count_all.Type == 'track', 'Type'] = 'Song'

#Create plot in figure - songs and podcasts listened per month
song_podcast = sns.catplot(data = month_count_all, kind='bar',x='month_year', y='Minutes_Played', hue='Type',ci=None,
                           palette='dark', alpha = .8, height=10, legend=False
                          )
#Plot title
song_podcast.fig.suptitle('Total Length of Songs and Podcasts Listened per Month', fontsize=20, fontweight=750)
#x-axis ticks and labels
ax.set_xticks(label_loc)
song_podcast.set_xticklabels(labels = xlabels, rotation = 75, fontsize=16)
#legend settings
plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0, fontsize=16)
plt.ylabel('Total Minutes Listened', fontsize=26, labelpad=10)
#Remove grid lines
plt.grid(b=False, which='both',axis='both')
#Remove x-axis label
song_podcast.set(xlabel=None)

plt.show()

'''Moving on to total minutes of songs vs. podcasts per day of the week.'''
#This is very similar to by month, just grouping by day_of_week rather than month
dow_count_all = (clean_full_df[['Type','day_of_week', 'Minutes_Played']].groupby(['Type','day_of_week'])
                 .sum().sort_values('day_of_week')).reset_index()
dow_count_all.loc[dow_count_all.Type == 'episode', 'Type'] = 'Podcast'
dow_count_all.loc[dow_count_all.Type == 'track', 'Type'] = 'Song'

#Day of week tick labels
dow_labels = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

#Create plot in figure
dow_habits = sns.catplot(data = dow_count_all, kind='bar',x='day_of_week', y='Minutes_Played', hue='Type',ci=None,
                           palette='dark', alpha = .8, height=10, hue_order = ['Podcast','Song'], legend = False
                          )
#Plot title
dow_habits.fig.suptitle('Podcasts and Songs Listened by Day of the Week', fontsize=20, fontweight=750)
#x-axis tick labels and remove axis label
dow_habits.set_xticklabels(dow_labels, rotation = 70, fontsize=16)
dow_habits.set(xlabel=None)
#Legend settings
plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0, fontsize=16)
#y-axis label
plt.ylabel('Total Minutes Listened', fontsize=26, labelpad=10)
#Remove grid lines
plt.grid(b=False, which='both',axis='both')
plt.show()

'''Moving on to total minutes of songs vs. podcasts by time of the day.'''
#Time of day dataframe and plot
tod_count_all = clean_full_df[['Type','Time of Day','Minutes_Played']].groupby(['Type','Time of Day']).sum().sort_values('Time of Day').reset_index()
tod_count_all.loc[tod_count_all.Type == 'episode', 'Type'] = 'Podcast'
tod_count_all.loc[tod_count_all.Type == 'track', 'Type'] = 'Song'
tod_count_all.sort_values('Time of Day', inplace=True)

#Column order
column_order = ['0-4','4-8','8-12','12-16','16-20','20-24']
#Time of day x axis tick labels
tod_x_labels = ['12AM-4AM', '4AM-8AM', '8AM-12PM','12PM-4PM','4PM-8PM','8PM-12AM']
#x tick axis locations
tod_label_loc = np.arange(len(tod_x_labels))

tod_habits = sns.catplot(data = tod_count_all, kind='bar',x='Time of Day', y='Minutes_Played', hue='Type',ci=None,
                           palette='dark', alpha = .8, height=10, hue_order = ['Podcast','Song'], order=column_order,
                         legend = False
                          )
#Remove grid lines
plt.grid(b=False, which='both',axis='both')
#Plot title
tod_habits.fig.suptitle('Podcasts and Songs Listened by Time of Day', fontsize=20, fontweight=750)
#x-axis tick settings
ax.set_xticks(tod_label_loc)
tod_habits.set_xticklabels(labels = tod_x_labels, rotation = 60, fontsize=20)
tod_habits.set(xlabel=None)
#legend settings
plt.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0, fontsize=16)
#y-axis label
plt.ylabel('Total Minutes Listened', fontsize=26, labelpad=10)
plt.show()
