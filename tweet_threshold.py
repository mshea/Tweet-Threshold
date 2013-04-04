import tweepy
import sqlite3
import json
import re
import time
import datetime
import math
import jinja2

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
				'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', 
						tweet.text).strip()
		text = re.sub('\:$','',text)
		try:
			url = tweet.entities['urls'][0]['expanded_url']
		except IndexError:
			url = False
		created_at = str(tweet.created_at).replace(' ','T')
		retweet_count = tweet.retweet_count
		screen_name = tweet.user.screen_name
		followers_count = tweet.user.followers_count
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
	full_results = []
	tweetquery = conn.cursor()
	tweetquery.execute('''
			select * from tweets 
			where datetime(created_at) > date('now','-7 day')
			;''')
	for result in tweetquery:
		id, text, url, created_at, retweet_count, screen_name, \
			followers_count = result
		full_results.append(result)
	return full_results
	
def get_score(retweet_count, followers_count): # The secret sause algorithm
	retweet_count -= 1 # lower score for low-follower users
	if retweet_count > 2:
		retweet_score = pow(retweet_count, 1.5) # boost retweets
		raw_score = (retweet_score / followers_count)*100000 # Build score
		score = round(math.log(raw_score, 1.09)) # Smooth out score
	else:
		score = 0
	return score

def build_html_page(data, html_template, html_output_file, threshold, 
		whitelist, blacklist):
	scored_tweets = []
	yesterdays_items = []
	last_weeks_items = []
	last_week_item_counter = 40
	yesterday = (datetime.datetime.today() - datetime.timedelta(days=1)) \
			.replace(hour=0, minute=0, second=0, microsecond=0)
	for item in data:
		id, text, url, created_at, retweet_count, screen_name, \
			followers_count = item
		score = get_score(retweet_count, followers_count)
		scored_tweets.append((text, url, score, screen_name, created_at, 
				retweet_count, followers_count))
	sorted_tweets = sorted(scored_tweets, key=lambda 
			tup: tup[2], reverse=True)
	for item in sorted_tweets:
		text, url, score, screen_name, created_at, retweet_count, \
				followers_count = item
		created_at_object = datetime.datetime.strptime(created_at, 
				'%Y-%m-%dT%H:%M:%S').replace(hour=0, minute=0, 
				second=0, microsecond=0)
		formatted_time = time.strftime('%I:%M %p', 
				time.strptime(created_at, '%Y-%m-%dT%H:%M:%S'))
		if ((score >= threshold or check_whitelist(screen_name, whitelist))
				and yesterday == created_at_object 
				and check_blacklist(text, blacklist)):
			yesterdays_items.append({'text': text.strip(), 'url': url, 
					'score': str(int(score)), 'screen_name': screen_name, 
					'created_at_time': formatted_time, 
					'retweet_count': retweet_count, 
					'followers_count': followers_count})
		if ((score >= threshold or check_whitelist(screen_name, whitelist))
				and created_at_object < yesterday 
				and last_week_item_counter > 0
				and check_blacklist(text, blacklist)):
			last_weeks_items.append({'text': text, 'url': url, 
					'score': str(int(score)), 'screen_name': screen_name, 
					'created_at_time': formatted_time, 
					'retweet_count': retweet_count, 
					'followers_count': followers_count})
			last_week_item_counter -= 1
	with open(html_template) as f: 
		template = jinja2.Template(f.read())
	html_output = template.render(yesterdays_items = yesterdays_items, 
			last_weeks_items = last_weeks_items)
	with open(html_output_file, 'w') as f: 
		f.write(html_output.encode('utf-8'))
	return True

def check_blacklist(text, BLACKLIST):
	for phrase in BLACKLIST:
		if phrase.strip() in text:
			return False
	return True
	
def check_whitelist(screen_name, WHITELIST):
	for whitelist_name in WHITELIST:
		if screen_name == whitelist_name:
			return True
	return False
	
def purge_database(db_file):
	conn = sqlite3.connect(db_file)
	cleandatabase = conn.cursor()
	cleandatabase.execute('''
			delete from tweets
			where datetime(created_at) < date('now','-8 day');
			''')
	cleandatabase.execute('vacuum;')
	conn.commit()