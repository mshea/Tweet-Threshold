import tweet_threshold

TWITTER_ACCOUNT_DATA = [
    {'consumer_key': 'accountkey',
     'consumer_secret': 'accountkey',
     'access_token_key': 'accountkey',
     'access_token_secret': 'accountkey'},
    {'consumer_key': 'accountkey',
     'consumer_secret': 'accountkey',
     'access_token_key': 'accountkey',
     'access_token_secret': 'accountkey'}]

PARAMS = {
    'db': '/path/to/your/dir/tweet_threshold.sqlite',
    'html_output': '/path/to/your/dir/index.html',
    'html_template': '/path/to/your/dir/html_template.txt',
    'rss_output_file': '/path/to/your/dir/yesterday.xml',
    'json_output_file': '/path/to/your/dir/items.json',
    'threshold': 50,
    'blacklist': (
        'Congress',
        'Representative',
        'DHS',
        'Fox',
        'CISPA',
        'Republicans',
        '[Sponsor]'),
    'whitelist': (
        'mshea',
        'slyflourish',
        'yourwife',
        'yourbestfriend')}

tweet_threshold.main(TWITTER_ACCOUNT_DATA, PARAMS)
