import tweet_threshold

PARAMS = {
	'DB_FILE': '/usr/www/users/pl569/cgi-bin/twitter/tweet_threshold.sqlite',
	'JSON_FILE': '/usr/www/users/pl569/news/data.js',
	'SCORE_THRESHOLD': 50,
	'BLACKLIST': [
			'Congress', 
			'Representative',
			'DHS', 
			'Fox', 
			'CISPA',
			'Republicans'
		],
	'HTML_TEMPLATE': '/usr/www/users/pl569/cgi-bin/twitter/html_template.txt',
	'HTML_OUTPUT': '/usr/www/users/pl569/news/index.html'
		
}

TWITTER_ACCOUNT_DATA = [
	{
	'consumer_key': 'wOBytOAodUNAsJH71cbBvg',
	'consumer_secret': 'K1xkHtnIQcnkxbhRkTNOOEsI3OLDZoIMdQAY9b4Tl0Q',
	'access_token_key': '779171-5VhTJzDLrJD9l661f6sa80QVSikwxRMzhSufOXU5Egk',
	'access_token_secret': 'By99ZpVCo6YQ5Iqord5nmZ3ZL8Pg4Io3UnTeLZdZc',
	}, {
	'consumer_key': 'h5ZDF4N8qSQu6qKRYzIqpA',
	'consumer_secret': 'XqsDsvZSuFzHgt03WuCzL5VSzkqm4BidtUMyFaxAjk',
	'access_token_key': '27217974-9rBMkdIP1JJiaSdzFBkXEbcmJPHcJVMTUWQnAO5kp',
	'access_token_secret': 'i9eVMn9Ssv4IthNZt3oJillB189lwEGEESQf3C8Q',
	}
]

def main(TWITTER_ACCOUNT_DATA, PARAMS):
	for account in TWITTER_ACCOUNT_DATA:
		tweets = tweet_threshold.get_tweets(account)
		tweet_threshold.export_to_sqlite(tweets, PARAMS['DB_FILE'])
	output_tweets = tweet_threshold.load_tweets_from_sqlite(PARAMS['DB_FILE'])
	tweet_threshold.export_to_json(output_tweets, PARAMS['JSON_FILE'], 
			PARAMS['SCORE_THRESHOLD'], PARAMS['BLACKLIST'])
	tweet_threshold.build_html_page(output_tweets, PARAMS['HTML_TEMPLATE'],
			PARAMS['HTML_OUTPUT'], PARAMS['SCORE_THRESHOLD'])
	tweet_threshold.purge_database(PARAMS['DB_FILE'])

if __name__ == "__main__":
    main(TWITTER_ACCOUNT_DATA, PARAMS)
