# spotify_who_am_i

## Intro  
Spotify has changed the way I listen to music and podcasts, the way I interact with and keep in touch with friends, and is tool that I use almost every single day. After finding out that I could request my listening history data from Spotify and use their API to collect additional information on the tracks and artists I listened to I had dig deeper to learn about myself as a Spotify user. A number of people have analyzed the attributes of the songs they listened to, and I did as well, but I wanted to specifically investigate how my listening habits changed over time and when I listened to songs and podcasts on Spotify. I was curious to contextualize what I already knew, that spotify was a big part of my audio consumming life, and deepen that understanding 

This repository contains the code necessary to retrieve the track type, artist info, and song attributes for your listening history or for a playlist on Spotify given the playlist id. With that information code is presented to create a categorical line chart visualizing song attributes over time, bar charts of the day of the week and time of day songs and podcasts are consumed, and kde plots of song attributes comparing an individidual to the USA's top 50 songs. 

The packages used in this analysis are: pandas, matplotlib, seaborn, spotipy, datetime, ast, time, and os. 

## Requesting Initial Data from Spotify
1. Go to [spotify.com](https://www.spotify.com/us/home/) and log in to your account
2. Go to your profile
3. From the menu on the left side of the screen select 'Privacy Settings'
4. Scroll to the bottom of the page and click on the green "Request" button
5. Confirm that you would like to recieve your data in the email Spotify will send
6. Wait for your data to arrive via email. Spotify says it will take up to 30 days, but it is usually much faster. When it arrives unzip the folder and place the MyData folder in your project folder and do not change the name of the folder. 

## Get your Client and Secret iD via Spotify for Developers
To access the Spotify API you will need to connect Spotify Developer to your Spotify Account
1. Either log into your Spotify Developer account or sign up [here](https://developer.spotify.com/dashboard/login).
2. Access your Develop Dashboard
3. Create a new app. Note, you cannot monetize apps created with the API
4. Click on your app and you'll see your client id at the top and the option to toggle your secret id visible. You'll need these both in the next step: configuring the settings. 

## Settings
There are a few variables you can set based on your preferences and timezone. Those variables are set in `settings.py` and are summarized below: <br>
- change_timezone - Spotify sends the time data in the UTC timezone. If you would like to change the time zone leave this True. Otherwise, set it False <br>
- timezone_change_start - The first date in a range to change the time (if change_timezone is True). Format: 'YYYY-MM-DD' <br>
- timezone_change_end - The end day for the time zone change range <br>
- hours_different - The number of hours to change the timezone by. Should be negative if behind UTC time, positive if ahead. <br>
- trim_first_month - If the first month of data is short and not ideal for monthly analysis, set True for it to be filtered before doing monthly analysis. <br>
- trim_last_month - Same as trim_first_month for the last month of the data.<br>
- song_attributes - List of attributes to compare the average of month over month. Note that if you change this all items of the list should be on the same scale as they will be plotted together. <br>
- song_attributes_2 - A shorter list of attributes to plot with each other by month. <br>
- song_attributes_3 - Another shorter list of attributes to plot with each other by month. <br>
### Private Settings
There are a couple of personal ids to keep private, your client_id and secret_id. These are found in your Spotify Developer app as discussed earlier. Create a file called `private.py` in your working folder and create two variables: client_id, and client_secret with you client id and secret id stored to them respectively. 

## Preparing Python
1. Install Python 3 via Anaconda or other method. 
2. In command line run `pip install -r requirements.txt` to install the required packages.

## Retrieve and Visualize Data
### Retrieving the Track Attributes
1. Run `python spot_retrieve.py`. Depending on how many tracks are in your listening history this may take a while and a consitent internet connection is important. Upon comleting two csv files will be created in your project folder: <br>
'full_streaming_history.csv' -  This will contain your full listening history as Spotify sent it to you.<br>
'listening_history_unique_songs.csv' - This will contain one entry for each unique track in your history along with all of the collected song and artist information. <br>
'track_play_counts.csv' - This file will contain a mapping of each unique track with the number of times they appeared (were played) in your listening history. I did not use this file in my analysis for this project, but is useful information if you want to do further analysis. <br>
### Listening History Analysis
1. Run `python spot_analysis.py`. This script will calculate some basic summary statistics of your listening history and visualize the following: <br> 
- The monthly average of song attributes of the songs you listened to over the course of the length of the data.<br>
- The total number of minutes of songs and podcasts listened to on a monthly basis. <br>
- The total number of minutes of songs and podcasts listened to on a day of the week basis. <br>
- The total number of minutes of songs and podcasts listened to on a time of day basis. 

## Possible Additional Areas of Investigation
1. Whether these types of patterns are typical, or if other people are more consistent in their patterns over time.
2. Compare attribute correlations between people to see if the correlations in my listening history hold up on a larger scale.
3. How my listening history attribute profile compares to popular playlists.
4. Compare volume of songs to their attributes. As the amount listened to goes up, do certain song attributes go up or down with it?
5. Repeating this analysis with a longer time frame. One year, particularily this strange year, is not totally representive of an individuals overall tendencies. 
6. Run a regression analysis to see if any variation in number of plays wer song can be explained by the song attributes.


## Credit
- Vlad Gheorge's [project](https://github.com/vlad-ds/spoty-records) was immensely helpful in the data retrieval process of this project. If you are interested in retrieving additional data specific to a user (e.g. tracks in a user's playlist) I recommend checking it out as he covers the Authorization Code Flow required for that process. 
- The documentation for [spotipy](https://spotipy.readthedocs.io/en/2.18.0/) documentation is also helpful in that regard, and for requesting many other pieces of information from Spotify.
- Spotiy also has great documentation for their [API](https://developer.spotify.com/documentation/web-api/) which is absolutely worth checking out. 
