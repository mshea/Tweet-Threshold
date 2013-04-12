import tweepy
import sqlite3
import json
import re
import time
import datetime
import math
import jinja2
import PyRSS2Gen


class Tweets (object):
    def __init__(self, account_data, params):
        auth = tweepy.auth.OAuthHandler(account_data['consumer_key'],
                account_data['consumer_secret'])
        auth.set_access_token(account_data['access_token_key'],
                account_data['access_token_secret'])
        api = tweepy.API(auth)
        self.db = params['db']
        self.tweets = []
        for tweet in api.home_timeline(count=100, include_rts=0):
            try:
                url = tweet.entities['urls'][0]['expanded_url']
            except IndexError:
                url = False
            if (url is not False):
                self.tweets.append((
                        tweet.id_str,
                        self.extract_urls(tweet.text),
                        url,
                        str(tweet.created_at).replace(' ', 'T'),
                        tweet.retweet_count,
                        tweet.user.screen_name,
                        tweet.user.followers_count
                        ))

    def save(self):
        tdb = TweetDatabase(self.db)
        tdb.save(self.tweets)
        tdb.purge()

    def extract_urls(self, text):
        text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '',
                text).strip()
        text = re.sub('\:$', '', text)
        return text

class TweetDatabase (object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()
        
    def create(self):
        try:
            self.c.execute('''CREATE TABLE tweets
                                    ( id int not null unique,
                                    text text,
                                    url text,
                                    created_at text,
                                    retweet_count int,
                                    screen_name text,
                                    followers_count int);''')
            self.conn.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def load(self):
        return self.c.execute('''select * from tweets;''')
    
    def save(self, data):
        self.create()
        self.c.executemany('''INSERT OR REPLACE INTO tweets 
                    VALUES (?,?,?,?,?,?,?)''', data)
        self.conn.commit()
        return True
        
    def purge(self):
        self.c.execute('''
            delete from tweets
            where datetime(created_at) < date('now','-8 day');
            ''')
        self.c.execute('vacuum;')
        self.conn.commit()
        return True

    
class FilteredTweets (object):
    def __init__(self, params):
        self.filtered_tweets = []
        self.blacklist = params['blacklist']
        self.whitelist = params['whitelist']
        self.db = TweetDatabase(params['db'])
        self.tweets = self.db.load()
        for tweet in self.tweets:
            id, text, url, created_at, retweet_count, screen_name, \
                    followers_count = tweet
            score = self.build_score(retweet_count, followers_count)
            if (self.check_blacklist(text) and (
                    score > params['threshold'] or 
                    self.check_whitelist(screen_name))):
                self.filtered_tweets.append(
                        {
                        'id': id, 
                        'text': text, 
                        'url': url, 
                        'created_at': created_at,
                        'retweet_count': retweet_count, 
                        'screen_name': screen_name, 
                        'followers_count': followers_count, 
                        'score': score
                        })
            self.filtered_tweets = sorted(self.filtered_tweets, key=lambda 
                    tup: tup['score'], reverse=True)

    def check_blacklist(self, text):
        for phrase in self.blacklist:
            if phrase.strip() in text:
                return False
        return True
    
    def check_whitelist(self, screen_name):
        for whitelist_name in self.whitelist:
            if screen_name == whitelist_name:
                return True
        return False

    def build_score(self, retweet_count, followers_count):
        retweet_count -= 1
        if retweet_count > 2:
            retweet_score = pow(retweet_count, 1.5)
            raw_score = (retweet_score / followers_count)*100000
            score = round(math.log(raw_score, 1.09))
        else:
            score = 0
        return int(score)

    def load_by_date(self, close, far):
        self.date_filtered_tweets=[]
        counter = 0
        for tweet in self.filtered_tweets:
            self.created_at_object = datetime.datetime.strptime(
                    tweet['created_at'], '%Y-%m-%dT%H:%M:%S')
            if (self.created_at_object > self.build_date(far) 
                    and self.created_at_object < self.build_date(close)
                    and counter < 40):
                self.date_filtered_tweets.append(tweet)
                counter += 1
        return self.date_filtered_tweets

    def build_date(self, day_delta):
        filter_date = (
                datetime.datetime.today() - 
                datetime.timedelta(days=day_delta)).replace(
                        hour=0, minute=0, second=0, microsecond=0)
        return filter_date
    
class Output (object):

    def build_webpage(self, yesterdays_items, last_weeks_items, params):
        with open(params['html_template']) as f: 
            template = jinja2.Template(f.read())
        self.html_output = template.render(yesterdays_items = yesterdays_items, 
                last_weeks_items = last_weeks_items)
        with open(params['html_output'], 'w') as f: 
            f.write(self.html_output.encode('utf-8'))
        return True
        
    def build_rss(self, items, output_file):
        rss_items = []
        sorted_items = sorted(items, key=lambda 
                    tup: tup['created_at'], 
                    reverse=True)
        for item in sorted_items:
            rss_items.append(PyRSS2Gen.RSSItem(
                    title = '%s: %s - Score: %s' % (
                        item['screen_name'],
                        item['text'],
                        item['score']),
                    link = item['url'],
                    pubDate = datetime.datetime.strptime(
                            item['created_at'], '%Y-%m-%dT%H:%M:%S')))
        rss = PyRSS2Gen.RSS2(
            title = 'Mike\'s News',
            link = 'http://mikeshea.net/news/',
            description = 'Mike\'s personal news filtered by Tweet Threshold.',
            lastBuildDate = datetime.datetime.now(),
            items = rss_items
        )
        with open(output_file, 'w') as f:
            rss.write_xml(f)
        return True
        
    def build_json(self, items, output_file):
        with open(output_file, 'w') as f:
            f.write(json.dumps(items))
        return True
        
def main(accounts, params):
    for account in accounts:
        remote_tweets = Tweets(account, params)
        remote_tweets.save()
    tweets = FilteredTweets(params)
    wp = Output()
    wp.build_webpage(tweets.load_by_date(0,1), tweets.load_by_date(1,6), params)
    wp.build_rss(tweets.load_by_date(0,1), params['rss_output_file'])
    wp.build_json(tweets.load_by_date(0,7), params['json_output_file'])