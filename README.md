> "The most essential service of the next decade will be the one that keeps you the best informed in the least amount of time. Theres more to life than staring at screens all day."

\- [Mike Davidson, VP of design, Twitter, and founder, Newsvine](http://alistapart.com/article/what-we-learned-in-2012)

The line between content producers and advertisers grows thin. All content creators demand your attention, whether they be J.J. Abrams and his Star Wars movie or your niece and her Facebook post about her dog's anxiety problem. As content becomes easier to produce and distribute, we need better tools to help us filter what we want from the sea of noise trying to get at us. This [Tweet Threshold Python script posted to Github](https://github.com/mshea/Tweet-Threshold) is an experiment in automatically filtering tweets pulled from a list of Twitter accounts based on a Threshold.

You can download the [Tweet Threshold Python script at Github](https://github.com/mshea/Tweet-Threshold) and run it yourself anywhere you can run Python. I've released it under a [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 license](http://creativecommons.org/licenses/by-nc-sa/3.0/) so you can distribute it, modify it, and share it as long as you release it under a similar license and attribute the original program to me.

## What This Script Does

This script reaches out to Twitter and pulls down the latest 100 tweets in JSON from your timeline. It then saves any tweets that meet a minimum threshold of 10 retweets per 100,000 followers (.01% retweet / followers) in a local SQLite3 database. From this database, the script outputs a [JSON file](http://www.json.org). The JSON file can be loaded into am HTML page that uses [JQuery](http://jquery.com) and [Moments.js](http://momentjs.com) to display the results. Here is an example in my [Tweet News page](http://mikeshea.net/twitter/).

## How to Use This Script

You'll want some experience working with Python and Javascript to run these scripts. They use a set of Python plugins to handle the authentication to Twitter for your timeline. These plugins include [httplib2](http://code.google.com/p/httplib2/), [Oauth2](https://github.com/simplegeo/python-oauth2), and [Python-twitter](https://github.com/bear/python-twitter).

You'll need to register this script as an application with Twitter. See [https://dev.twitter.com/apps](https://dev.twitter.com/apps) for more information.

Change the parameters in "fetch_tweets.py" to your own twitter authentication codes and the local directories where you want the results. Modify the HTML file to suit your needs. Set up a scheduled event like a cronjob to run "fetch_tweets.py" once every hour.

## A Small Solution to a Growing Problem

We're going to need better agents like this if we want to take back our attention from the hordes of content producers demanding their space in our brains. I'm hoping to continue working on this problem or finding better solutions. We can't trust the big companies like Twitter or Google to do this for us. It isn't in their interests to help us avoid using their sites. We can only trust our own tools and our ourselves to do it for us.

If you're interested in this topic, know of some other tools like this, or have used the script and found it useful, please send me an email to mike@mikeshea.net to let me know.