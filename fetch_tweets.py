import tweet_threshold

PARAMS = {
	'DB_FILE': '/path/to/your/db/tweet_threshold.sqlite',
	'HTML_TEMPLATE': '/path/to/your/www/html_template.txt',
	'HTML_OUTPUT': '/path/to/your/www/index.html'
	'SCORE_THRESHOLD': 50,
	'BLACKLIST': [
			'Congress', 
			'Representative',
			'DHS', 
			'Fox', 
			'CISPA',
			'Republicans'
		],
	'WHITELIST': [
			'twitter_account_you_like',
			'twitter_account_you_like',
			'twitter_account_you_like'
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
	tweet_threshold.build_html_page(
			output_tweets, 
			PARAMS['HTML_TEMPLATE'],
			PARAMS['HTML_OUTPUT'], 
			PARAMS['SCORE_THRESHOLD'], 
			PARAMS['WHITELIST'],
			PARAMS['BLACKLIST'])
	tweet_threshold.purge_database(PARAMS['DB_FILE'])

if __name__ == "__main__":
    main(TWITTER_ACCOUNT_DATA, PARAMS)