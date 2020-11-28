# twitter-bot-music-insights
A Twitter bot that generates daily music insights powered by Chartmetric

## Motivation
As a data scientist with a passion for discovering new music and helping industry professionals, I created 5 python scripts that are each programmed to generate music insights. Each script, which is outlined below, is scheduled to run weekly on its designated day of the week. As today's music climate is becoming saturated with  more aspiring artists, staying on top of the latest trends and overnight, breakthrough talent is nearly impossible. So whether you're a music enthusiast or this is how you pay your rent, this project is meant to help you. The data source is powered by [Chartmetric](https://app.chartmetric.com/dashboard/artists)

Follow me [@jacksonabull](https://twitter.com/jacksonabull) to see the latest

## KPIs
**Velocity**: Average Change in Rank over 7-day Period

**Spotify Popularity**: The value will be between 0 and 100, with 100 being the most popular. The artist’s popularity is calculated from the popularity of all the artist’s tracks.

## Bot Information
### `bot1.py`
**Schedule:** *Monday @ 13:30 UTC, Weekly*

**Insights Description:** This bot collects data on the top 100 trending tracks of the week on Tiktok and finds the record with the highest velocity (most viral track)
### `bot2.py`
**Schedule:** *Tuesday @ 17:00 UTC, Weekly*

**Insights Description:** This bot collects data on the top 100 trending tracks of the week on Shazam and finds the record with the highest velocity (most viral track)
### `bot3.py`
**Schedule:** *Wednesday (first) @ 12:00 UTC, Monthly*

**Insights Description:** This bot collects data on the top trending tracks on Tiktok from the previous 4 weeks. For each unique artists, the bot will collect daily listener counts for the current day *and* the date 7-days earlier. Based on the difference between those two values, the bot will output metadata for the artist with the biggest gain in listeners.

**How It Works:**
1. Collects data for the top 100 trending tracks on Tiktok for each week over the past month
2. Drops any track without an isrc code in order to filter out any audio that's not an actually song (i.e. some random user-generated audio)
3. Drop all duplicate artists except for the last occurrence 
4. Using the ID for each artist, I fetch historical values for Spotify listeners and extract the first and last values to create a tuple.
5. Feature engineer a new `listener difference` column calculated by subtracting the first tuple item from the second tuple item
6. Sort DataFrame by `listener difference` in descending order
7. Grab relevant data from first row to include in Tweet message
### `bot4.py`
**Schedule:** *Thursday @ 14:00 UTC, Weekly*

**Insights Description:** A fun, throwback-thursday post to reminisce the #1 song on Spotify's Top 200 a year ago.

### `bot5.py`
**Schedule:** *Friday @ 12:00 UTC, Weekly*

**Insights Description:** Similar to Wednesday's monthly post, this bot focuses on the artist with the biggest *weekly* boost in Spotify listeners

**How It Works:** *Same process as Wednesday except within a scope of 1 week*

### `bot6.py`
**Schedule:** *Wednesday(second) @ 12:00 UTC, Monthly*

**Insights Description:** This bot collects data on 4 weeks of tiktok's top tracks. For each unique artist, the program calculates the total wikipedia views, returning the artist with the most wikipedia views. 


