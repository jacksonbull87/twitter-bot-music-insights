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
### Wednesday `tiktok_spot_growth(monthly).py`
**Description:** Identifies which trending-artist on TikTok experienced the biggest monthly gain in Spotify listeners
**How It Works:**
1. Collects data for the top 100 trending tracks on Tiktok for each week over the past month
2. Drops any track without an isrc code in order to filter out any audio that's not an actually song (i.e. some random user-generated audio)
3. Drop all duplicate artists except for the first occurrence 
4. Using the ID for each artist, I fetch historical values for Spotify listeners and extract the first and last values to create a tuple.
5. Feature engineer a new `listener difference` column calculated by subtracting the first tuple item from the second tuple item
6. Sort DataFrame by `listener difference` in descending order
7. Grab relevant data from first row to include in Tweet message
### Thursday `num1song_tweet.py`
A throwback Thursday themed post for the number 1 song a year ago on the Spotify Top 200 Chart
### Friday `tiktok_spot_growth(weekly).py`
**Description:** Similar to Wednesday's monthly post, this bot focuses on the artist with the biggest *weekly* boost in Spotify listeners
**How It Works:** *Same process as Wednesday except dont for one weekly chart*

