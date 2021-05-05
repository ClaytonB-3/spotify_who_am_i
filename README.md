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
1. Either log into your Spotify Developer account or sign up (here)[https://developer.spotify.com/dashboard/login].
2. Access your Develop Dashboard
3. Create a new app. Note, you cannot monetize apps created with the API
4. Click on your app and you'll see your client id at the top and the option to toggle your secret id visible. You'll need these both in the next step: configuring the settings. 

## Settings
There are a few variables you can set based on your preferences and timezone. Those variables are set in `settings.py` and are summarized below: <br>
change_timezone - Spotify sends the time data in the UTC timezone. If you would like to change the time zone leave this True. Otherwise, set it False <br>
timezone_change_start - The first date in a range to change the time (if change_timezone is True). Format: 'YYYY-MM-DD' <br>
timezone_change_end - The end day for the time zone change range <br>
hours_different - The number of hours to change the timezone by. Should be negative if behind UTC time, positive if ahead. <br>
trim_first_month - If the first month of data is short and not ideal for monthly analysis, set True for it to be filtered before doing monthly analysis. <br>
trim_last_month - Same as trim_first_month for the last month of the data.<br>
song_attributes - List of attributes to compare the average of month over month. Note that if you change this all items of the list should be on the same scale as they will be plotted together. <br>
song_attributes_2 - A shorter list of attributes to plot with each other by month. <br>
song_attributes_3 - Another shorter list of attributes to plot with each other by month. <br>
### Private Settings
There are a couple of personal ids to keep private, your client_id and secret_id. These are found in your Spotify Developer app as discussed earlier. Create a file called `private.py` in your working folder and create two variables: client_id, and client_secret. 

## Retrieve and Visualize Data 

## Credit
- Vlad Gheorge's [project](https://github.com/vlad-ds/spoty-records) was immensely helpful in the data retrieval process of this project. If you are interested in retrieving additional data specific to a user (e.g. tracks in a user's playlist) I recommend checking it out as he covers the Authorization Code Flow required for that process. 
- The documentation for [spotipy](https://spotipy.readthedocs.io/en/2.18.0/) documentation is also helpful in that regard, and for requesting many other pieces of information from Spotify.
- Spotiy also has great documentation for their [API](https://developer.spotify.com/documentation/web-api/) which is absolutely worth checking out. 
