import tweet_threshold

PARAMS = {
	'DB_FILE': '/path/to/your/db/tweet_threshold.sqlite',
	'JSON_FILE': '/path/to/your/www/json/dir/data.js',
	'SCORE_THRESHOLD': 50,
	'BLACKLIST': [
			'Congress', 
			'Representative',
			'DHS', 
			'Fox', 
			'CISPA',
			'Republicans'
		]
}

TWITTER_ACCOUNT_DATA = [
	{
	'consumer_key': 'keyhash',
	'consumer_secret': 'keyhash',
	'access_token_key': 'keyhash',
	'access_token_secret': 'keyhash',
	}, {
	'consumer_key': 'keyhash',
	'consumer_secret': 'keyhash',
	'access_token_key': 'keyhash',
	'access_token_secret': 'keyhash',
	}
]

def main(TWITTER_ACCOUNT_DATA, PARAMS):
	for account in TWITTER_ACCOUNT_DATA:
		tweets = tweet_threshold.get_tweets(account)
		tweet_threshold.export_to_sqlite(tweets, PARAMS['DB_FILE'])
	output_tweets = tweet_threshold.load_tweets_from_sqlite(PARAMS['DB_FILE'])
	tweet_threshold.export_to_json(output_tweets, PARAMS['JSON_FILE'], 
			PARAMS['SCORE_THRESHOLD'], PARAMS['BLACKLIST'])
	tweet_threshold.purge_database(PARAMS['DB_FILE'])

if __name__ == "__main__":
    main(TWITTER_ACCOUNT_DATA, PARAMS)
