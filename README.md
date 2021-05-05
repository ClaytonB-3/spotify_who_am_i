# spotify_who_am_i

## Intro  
Spotify has changed the way I listen to music and podcasts, the way I interact with and keep in touch with friends, and is tool that I use almost every single day. After finding out that I could request my listening history data from Spotify and use their API to collect additional information on the tracks and artists I listened to I had dig deeper to learn about myself as a Spotify user. A number of people have analyzed the attributes of the songs they listened to, and I did as well, but I wanted to specifically investigate how my listening habits changed over time and when I listened to songs and podcasts on Spotify. I was curious to contextualize what I already knew, that spotify was a big part of my audio consumming life, and deepen that understanding 

This repository contains the code necessary to retrieve the track type, artist info, and song attributes for your listening history or for a playlist on Spotify given the playlist id. With that information code is presented to create a categorical line chart visualizing song attributes over time, bar charts of the day of the week and time of day songs and podcasts are consumed, and kde plots of song attributes comparing an individidual to the USA's top 50 songs. 

The packages used in this analysis are: pandas, matplotlib, seaborn, spotipy, datetime, ast, time, and os. 

## Requesting Initial Listening History from Spotify
1. Go to [spotify.com](https://www.spotify.com/us/home/) and log in to your account
2. Go to your profile
3. From the menu on the left side of the screen select 'Privacy Settings'
4. Scroll to the bottom of the page and click on the green "Request" button
5. Confirm that you would like to recieve your data in the email Spotify will send
6. Wait for your data to arrive via email. Spotify says it will take up to 30 days, but it is usually much faster. When it arrives unzip the folder and place all json files starting with 'StreamingHistory' to your project folder. 

## Get your Client and Secret iD via Spotify for Developers
To access the Spotify API you will need to connect Spotify Developer to your Spotify Account
1. Either log into your Spotify Developer account or sign up (here)[https://developer.spotify.com/dashboard/login].
2. Access your Develop Dashboard
3. Create a new app. Note, you cannot monetize apps created with the API
4. Click on your app and you'll see your client id at the top and the option to toggle your secret id visible. You'll need these both in the next step: configuring the settings. 

## Settings
There are a few personalizations you can make based on your preferences and timezone.

## Retrieve and Visualize Data 

## Credit
- Vlad Gheorge's [project](https://github.com/vlad-ds/spoty-records) was immensely helpful in the data retrieval process of this project. If you are interested in retrieving additional data specific to a user (e.g. tracks in a user's playlist) I recommend checking it out as he covers the Authorization Code Flow required for that process. 
- The documentation for [spotipy](https://spotipy.readthedocs.io/en/2.18.0/) documentation is also helpful in that regard, and for requesting many other pieces of information from Spotify.
- Spotiy also has great documentation for their [API](https://developer.spotify.com/documentation/web-api/) which is absolutely worth checking out. 
