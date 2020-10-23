# twitter-bot-music-insights
A Twitter bot that generates daily music insights powered by Chartmetric

## Motivation
As a data scientist with a passion for discovering new music and helping industry professionals, I created 5 python scripts that are each programmed to generate music insights. Each script, which is outlined below, is scheduled to run weekly on its designated day of the week. As today's music climate is becoming saturated with  more aspiring artists, staying on top of the latest trends and overnight, breakthrough talent is nearly impossible. So whether you're a music enthusiast or this is how you pay your rent, this project is meant to help you. The data source is powered by [Chartmetric](https://app.chartmetric.com/dashboard/artists)

Follow me [@jacksonabull](https://twitter.com/jacksonabull) to see the latest

## KPIs
**Velocity**: Average Change in Rank over 7-day Period

**Spotify Popularity**: The value will be between 0 and 100, with 100 being the most popular. The artist’s popularity is calculated from the popularity of all the artist’s tracks.

## Post Schedule
### Monday `viral_tiktok.py`
Posts song with the highest velocity  from this week's top 100 trending Tiktok tracks
### Tuesday `viral_shazam.py`
Posts song with the highest velocity  from this week's top 100 trending Shazam tracks
### Thursday `num1song_tweet.py`
A throwback Thursday themed post for the number 1 song a year ago on the Spotify Top 200 Chart
### Friday `best_emerging_artist_tweet.py`
Looking at the most current daily Spotify Top 200 chart, this script calculates the percent net gain/loss of popularity for each artist over 7-days. Posts artist with the biggest increase in popularity
