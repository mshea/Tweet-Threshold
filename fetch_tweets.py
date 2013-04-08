import tweet_threshold

TWITTER_ACCOUNT_DATA = [
	{
	'consumer_key': 'yourkeyhere',
	'consumer_secret': 'yourkeyhere',
	'access_token_key': 'yourkeyhere',
	'access_token_secret': 'yourkeyhere',
	}, {
	'consumer_key': 'yourkeyhere',
	'consumer_secret': 'yourkeyhere',
	'access_token_key': 'yourkeyhere',
	'access_token_secret': 'yourkeyhere',
	}
]
	
PARAMS = {
	'db': '/your/path/here/tweet_threshold.sqlite',
	'html_output': '/your/path/here/news.html',
	'html_template': '/your/path/here/html_template.txt',
	'blacklist': (
		'asdf',
		'asdfasdf'
		),
	'whitelist': (
		'mshea',
		'slyflourish'
		)
	}

tweet_threshold.main(TWITTER_ACCOUNT_DATA, PARAMS)