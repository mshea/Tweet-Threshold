# Note, this file requires the tweet_threshold python library.
# This file contains the parameters and instructions for fetching
# tweets from a twitter account and saving them to a local SQLite3 and
# JSON file.
#
# See https://github.com/mshea/Tweet-Threshold for more information.
#
# This script also requires that you register it as a twitter application
# See https://dev.twitter.com/apps for details.

import tweet_threshold

params = {
	'db_file': '/path/to/your/db/directory/tweets.sqlite',
	'consumer_key': 'yourkeyhere',
	'consumer_secret': 'yourkeyhere',
	'access_token_key': 'yourkeyhere',
	'access_token_secret': 'yourkeyhere',
	'json_output_file': '/path/to/your/json/output/directory/tweets.js',
	'threshold': 10, # number of retweets per 100,000 followers
	'minimum_retweets': 1 # minimum number of total retweets
	}

def main():
	tweets = tweet_threshold.fetch_tweets(params)
	tweet_threshold.dump_tweets_to_db(tweets, params)
	tweet_threshold.dump_json_file(tweets, params)
	tweet_threshold.purge_database(params)

if __name__ == "__main__":
    main()
    
