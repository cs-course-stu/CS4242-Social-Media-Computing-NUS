import os
import tweepy as tw
import pandas as pd
import csv

"""
Y29uc3VtZXJfa2V5ID0gJiMzOTtoVVRQQ240TVU0dFlGOFZmZHd4WWh2RUhZJiMzOTsNCmNvbnN1bWVyX3NlY3JldCA9ICYjMzk7MGM2R3lnQUlENGMzMElxd1BDQWJZUFJ2WUpsVWQ1NHRDaHBXSWNyT3lFbmprZmJ3YUEmIzM5Ow0KYWNjZXNzX3Rva2VuID0gJiMzOTsxMTM4NDIyMDQyMzUxMzc0MzM3LVNoOWNYU0o3SWpGMENuVWszcjFVcm1UVUxGUnUzTiYjMzk7DQphY2Nlc3NfdG9rZW5fc2VjcmV0ID0gJiMzOTsxSHlLZEpGRjVObHFLWnRTMlJ1bWFHY2lVaWUzc2FMT3hNaGxjYndHT2xMZHUmIzM5Ow==
"""

def judge_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)


class TweetCrawl:
    """ class TweetCrawl is a class dealing with crawling tweets
    Args:
        in_dir: working directory
        consumer_key: Twitter API: consumer_key
        consumer_secret: Twitter API: consumer_secret
        access_token: Twitter API: access_token
        access_token_secret: Twitter API: access_token_secret
    """

    def __init__(self, in_dir, consumer_key, consumer_secret, access_token, access_token_secret):
        self.in_dir = in_dir
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    """ get tweets from Twitter API
    Args:
        extend: shorten the tweet or not
        time: beginning time of cralwing
        item: number of tweets will be crawled
        expression: query search
    Returns:
        tweets: ItemIterator of tweets
    """

    def _get_tweet(self, extend, time, item, expression):
        if (extend == False):
            tweets = tw.Cursor(self.api.search, q=expression,
                               lang="en",
                               since=time,
                               include_entities=True
                               ).items(item)
        else:
            tweets = tw.Cursor(self.api.search, q=expression,
                               lang="en",
                               since=time,
                               tweet_mode="extended",
                               include_entities=True
                               ).items()
        return tweets

    """ crawl train text
    Args:
        extend: shorten the tweet or not
        time: beginning time of cralwing
        item: number of tweets will be crawled
        expression: query search
    """

    def crawl_train_text(self, extend, time, item, expression):
        file_dir = self.in_dir + 'input.train.text.csv'
        csvFile = open(file_dir, 'a+')
        csvWriter = csv.writer(csvFile)
        print("crawl training text data", end="")
        count = 0
        tweets = self._get_tweet(extend, time, item, expression)

        while True:
            try:
                tweet = tweets.next()
                count = count + 1
                if (count % 50 == 0):
                    print(".", end='', flush=True)
                str = ""
                if(tweet.entities['hashtags']):
                    for item in tweet.entities['hashtags']:
                        if not judge_pure_english(item['text']):
                            continue
                        str = str + ', ' + item['text']
                    str = str.replace(', ', '', 1)
                if((extend == False) and ("RT" not in tweet.text) and (str)):
                    csvWriter.writerow([tweet.text, str])
                if((extend == True) and ("RT" not in tweet.full_text) and (str)):
                    csvWriter.writerow([tweet.full_text, str])
            except tw.RateLimitError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        print("\n")

    """ crawl test text
    Args:
        extend: shorten the tweet or not
        time: beginning time of cralwing
        item: number of tweets will be crawled
    """

    def crawl_test_text(self, extend, time, item):
        file_dir = self.in_dir + 'input.test.text.csv'
        csvFile = open(file_dir, 'a+')
        csvWriter = csv.writer(csvFile)
        print("crawl testing text data", end="")
        count = 0
        tweets = self._get_tweet(extend, time, item)
        while True:
            try:
                tweet = tweets.next()
                count = count + 1
                print(count)
                if (count % 50 == 0):
                    print(".", end='', flush=True)
                str = ""
                if(tweet.entities['hashtags']):
                    for item in tweet.entities['hashtags']:
                        str = str + ', ' + item['text']
                    str = str.replace(', ', '', 1)
                if((extend == False) and ("RT" not in tweet.text) and not(str)):
                    csvWriter.writerow([tweet.text, str])
                if((extend == True) and ("RT" not in tweet.full_text) and not(str)):
                    csvWriter.writerow([tweet.full_text, str])
            except tw.RateLimitError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        print("\n")

    """ crawl train photo
    Args:
        time: beginning time of cralwing
        item: number of tweets will be crawled
    """

    def crawl_train_photo(self, time, item):
        file_dir = self.in_dir + 'input.train.photo.csv'
        csvFile = open(file_dir, 'a+')        
        csvWriter = csv.writer(csvFile)
        print("crawl training photo data", end="")
        count = 0
        tweets = self._get_tweet(False, time, item)
        while True:
            try:
                tweet = tweets.next()
                count = count + 1
                if (count % 50 == 0):
                    print(".", end='', flush=True)

                str_photo = ""
                if(("RT" not in tweet.text)):
                    if('media' in tweet.entities.keys()):
                        for item in tweet.entities['media']:
                            str_photo = str_photo + ', ' + \
                                item['media_url_https']
                str_photo = str_photo.replace(', ', '', 1)
                if (not str_photo):
                    continue  # filter out non-media tweet

                str_tag = ""
                if(tweet.entities['hashtags']):
                    for item in tweet.entities['hashtags']:
                        if not judge_pure_english(item['text']):
                            continue
                        str_tag = str_tag + ', ' + item['text']
                    str_tag = str_tag.replace(', ', '', 1)
                if(str_tag):
                    csvWriter.writerow([str_photo, str_tag])
            except tw.RateLimitError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        print("\n")

    """ crawl test photo
    Args:
        time: beginning time of cralwing
        item: number of tweets will be crawled
    """

    def crawl_test_photo(self, time, item):
        file_dir = self.in_dir + 'input.test.photo.csv'
        csvFile = open(file_dir, 'a+')        
        csvWriter = csv.writer(csvFile)
        print("crawl testing photo data", end="")
        count = 0
        tweets = self._get_tweet(False, time, item)
        while True:
            try:
                tweet = tweets.next()
                count = count + 1
                if (count % 50 == 0):
                    print(".", end='', flush=True)

                str_photo = ""
                if(("RT" not in tweet.text)):
                    if('media' in tweet.entities.keys()):
                        for item in tweet.entities['media']:
                            str_photo = str_photo + ', ' + \
                                item['media_url_https']
                str_photo = str_photo.replace(', ', '', 1)
                if (not str_photo):
                    continue  # filter out non-media tweet

                str_tag = ""
                if(tweet.entities['hashtags']):
                    for item in tweet.entities['hashtags']:
                        str_tag = str_tag + ', ' + item['text']
                    str_tag = str_tag.replace(', ', '', 1)
                if(not(str_tag)):
                    csvWriter.writerow([str_photo, str_tag])
            except tw.RateLimitError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
        print("\n")

if __name__ == '__main__':
    in_dir = '/Users/wangyifan/Desktop/'
    expression = "#friends OR #pets OR #tuesdaymotivation OR #funny OR #contest OR #giveaway OR #ootd OR #win OR #merrychristmas OR #competition OR #fridayfeeling OR #traveltuesday OR #happybirthday OR #wcw OR #goals OR #fitness OR #vegan OR #movies OR #running OR #thankful OR #science OR #blessed OR #influencer OR #metoo"
    tweet_crawl = TweetCrawl(
        in_dir, consumer_key, consumer_secret, access_token, access_token_secret)
    tweet_crawl.crawl_train_text(
        extend=True, time="2017-08-13", item=500000, expression=expression)
