# spotify_who_am_i

## Intro  
Spotify has changed the way I listen to music and podcasts, the way I interact with and keep in touch with friends, and is tool that I use almost every single day. After finding out that I could request my listening history data from Spotify and use their API to collect additional information on the tracks and artists I listened to I had dig deeper to learn about myself as a Spotify user. A number of people have analyzed the attributes of the songs they listened to, and I did as well, but I wanted to specifically investigate how my listening habits changed over time and when I listened to songs and podcasts on Spotify. I was curious to contextualize what I already knew, that spotify was a big part of my audio consumming life, and deepen that understanding 

This repository contains the code necessary to retrieve the track type, artist info, and song attributes for your listening history or for a playlist on Spotify given the playlist id. With that information code is presented to create a categorical line chart visualizing song attributes over time, bar charts of the day of the week and time of day songs and podcasts are consumed, and kde plots of song attributes comparing an individidual to the USA's top 50 songs. 

The packages used in this analysis are: pandas, matplotlib, seaborn, spotipy, datetime, ast, time, and os. 
