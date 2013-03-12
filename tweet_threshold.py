import tweepy
import sqlite3
import json
import re
import time
import math

def get_tweets(account_data):
	auth = tweepy.auth.OAuthHandler(account_data['consumer_key'],
			account_data['consumer_secret'])
	auth.set_access_token(account_data['access_token_key'],
			account_data['access_token_secret'])
	api = tweepy.API(auth)

	tweet_data = []
	for tweet in api.home_timeline(count=100, include_rts=0):
		id = tweet.id_str
		text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'\
				'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', tweet.text)
		try:
			url = tweet.entities['urls'][0]['expanded_url']
		except IndexError:
			url = False
		created_at = str(tweet.created_at).replace(' ','T')
		retweet_count = tweet.retweet_count * 1.0 # Create float
		screen_name = tweet.user.screen_name
		followers_count = tweet.user.followers_count * 1.0 # Create float
		if (url is not False):
			tweet_data.append((id, text, url, created_at, retweet_count, 
					screen_name, followers_count))
	return tweet_data

def export_to_sqlite(data, db_file):
	conn = sqlite3.connect(db_file)
	c = conn.cursor()
	try: # Data Model Below
		c.execute('''CREATE TABLE tweets 
				( id int not null unique,
				text text, 
				url text, 
				created_at text, 
				retweet_count int,
				screen_name text,
				followers_count int);''')
	except:
		error = "table already created..."
	c.executemany('''INSERT OR REPLACE INTO tweets VALUES (?,?,?,?,?,?,?)''', 
					data)
	conn.commit()
	return True

def load_tweets_from_sqlite(db_file):
	conn = sqlite3.connect(db_file)
	c = conn.cursor()
	results = []
	tweetquery = conn.cursor()
	tweetquery.execute('''
			select * from tweets 
			where datetime(created_at) > date('now','-7 day')
			;''')
	for result in tweetquery:
		id, text, url, created_at, retweet_count, screen_name, \
			followers_count = result
		results.append(result)
	return results
	
def get_score(retweet_count, followers_count): # The secret sause algorithm
	retweet_count -= 1 # lower score for low-follower users
	if retweet_count > 2:
		retweet_score = pow(retweet_count, 1.5) # boost retweets
		raw_score = (retweet_score / followers_count)*100000 # Build score
		score = round(math.log(raw_score, 1.09)) # Smooth out score
	else:
		score = 0
	return score

def export_to_json(data, json_file, SCORE_THRESHOLD, BLACKLIST):
	output = []
	for item in data:
		id, text, url, created_at, retweet_count, screen_name, \
			followers_count = item
		score = get_score(retweet_count, followers_count)
		clean_tweet = check_blacklist(text, BLACKLIST)
		if score >= SCORE_THRESHOLD and clean_tweet:
			output.append({'id': id, 'text': text, 'url': url, 
				'created_at': created_at, 'retweet_count': retweet_count,
				'screen_name': screen_name, 'followers_count': followers_count,
				'score': score})
	with open(json_file, "w") as json_output_handler:
		json_output_handler.write(json.dumps(output))

def check_blacklist(text, BLACKLIST):
	for phrase in BLACKLIST:
		if phrase.strip() in text:
			return False
	return True
	
def purge_database(db_file):
	conn = sqlite3.connect(db_file)
	cleandatabase = conn.cursor()
	cleandatabase.execute('''
			delete from tweets
			where datetime(created_at) < date('now','-8 day');
			''')
	cleandatabase.execute('vacuum;')
	conn.commit()

