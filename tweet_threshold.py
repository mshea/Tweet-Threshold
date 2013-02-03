# Tweet Threshold: A Python twitter client to help you find the most 
# interesting tweets in your stream. This script monitors your 
# stream, captures retweeted tweets, stores them in SQLite, and 
# outputs a json file suitable for display in a Jquery-based HTML page.
#
# This script requires the following non-default Python modules:
# httplib2: http://code.google.com/p/httplib2/
# Oauth2: https://github.com/simplegeo/python-oauth2
# Python-twitter: https://github.com/bear/python-twitter
#
# The HTML file that displays the results of this script uses the following
# two javascript modules:
#
# JQuery: http://jquery.com
# Moments.js for time formatting: http://momentjs.com
#
# For more information, please read http://mikeshea.net/tweet_threshold.html

import twitter
import sqlite3
import time
import json

def fetch_tweets(params):
	api = twitter.Api(consumer_key=params['consumer_key'],
                      consumer_secret=params['consumer_secret'],
                      access_token_key=params['access_token_key'],
                      access_token_secret=params['access_token_secret'])
	tweets = api.GetFriendsTimeline(count = 100)
	tweet_data = []
	for tweet in tweets:
		created_at_iso = convert_twitter_timestamp_to_sqlite(tweet.created_at)
		score = (tweet.retweet_count * 1.0 / tweet.user.followers_count * 1.0
				) * 100000
		if (score >= params['threshold'] and 
				tweet.retweet_count >= params['minimum_retweets']):
			tweet_data.append((tweet.id, tweet.text, tweet.created_at, 
					tweet.retweet_count, tweet.user.screen_name, 
					tweet.user.followers_count, created_at_iso))
	return tweet_data

def dump_tweets_to_db(tweet_data, params):
	conn = sqlite3.connect(params['db_file'])
	c = conn.cursor()
	try:
		c.execute('''CREATE TABLE tweets (id int not null primary key,
						text text, created_at text, retweet_count int, 
						screen_name text, follower_count int, 
						created_at_iso text);''')
	except:
		error = "table already created..."
	c.executemany('''INSERT OR REPLACE INTO tweets VALUES (?,?,?,?,?,?,?)''', 
					tweet_data)
	conn.commit()

def convert_twitter_timestamp_to_sqlite(created_at):
	tweet_time = time.strptime(created_at, 
			'%a %b %d %H:%M:%S +0000 %Y')
	timestring = time.strftime('%Y-%m-%dT%H:%M:%S', tweet_time)
	return timestring

def dump_json_file(db_file, params):
	conn = sqlite3.connect(params['db_file'])
	c = conn.cursor()
	tweets_json = []
	tweetquery = conn.cursor()
	tweetquery.execute('''
			select * from tweets 
			where text like '%http%'
			and datetime(created_at_iso) > date('now','-6 day') 
			order by created_at_iso desc;''')
	for result in tweetquery:
		id, text, created_at, retweet_count, screen_name, \
				follower_count, created_at_iso = result
		tweets_json.append({'id_str': str(id), 'text': text, 'created_at': 
				created_at, 'retweet_count': retweet_count, 'screen_name': 
				screen_name, 'follower_count': follower_count, 'created_at_iso':
				created_at_iso})
		with open(params['json_output_file'], "w") as json_output_handler:
			json_output_handler.write(json.dumps(tweets_json))

def purge_database(params):
	conn = sqlite3.connect(params['db_file'])
	cleandatabase = conn.cursor()
	cleandatabase.execute('''
			delete from tweets
			where datetime(created_at_iso) < date('now','-14 day');
			''')
	cleandatabase.execute('vacuum;')
	conn.commit()