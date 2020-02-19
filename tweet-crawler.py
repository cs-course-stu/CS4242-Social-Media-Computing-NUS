import os
import tweepy as tw
import pandas as pd
import csv

"""
Y29uc3VtZXJfa2V5ID0gJiMzOTtoVVRQQ240TVU0dFlGOFZmZHd4WWh2RUhZJiMzOTsNCmNvbnN1bWVyX3NlY3JldCA9ICYjMzk7MGM2R3lnQUlENGMzMElxd1BDQWJZUFJ2WUpsVWQ1NHRDaHBXSWNyT3lFbmprZmJ3YUEmIzM5Ow0KYWNjZXNzX3Rva2VuID0gJiMzOTsxMTM4NDIyMDQyMzUxMzc0MzM3LVNoOWNYU0o3SWpGMENuVWszcjFVcm1UVUxGUnUzTiYjMzk7DQphY2Nlc3NfdG9rZW5fc2VjcmV0ID0gJiMzOTsxSHlLZEpGRjVObHFLWnRTMlJ1bWFHY2lVaWUzc2FMT3hNaGxjYndHT2xMZHUmIzM5Ow==
"""
def judge_pure_english(keyword):
    return all(ord(c) < 128 for c in keyword)


class TweetCrawler:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    def get_tweet(self, extend, time, item):
        if (extend == False):
            tweets = tw.Cursor(self.api.search, q="*",
                                    lang="en",
                                    since=time,
                                    ).items(item)
        else:
            tweets = tw.Cursor(self.api.search, q="*",
                                    lang="en",
                                    since=time,
                                    tweet_mode="extended"
                                    ).items(item)
        return tweets

    def crawler_train_text(self, extend, time, item):
        csvFile = open('input.train.text.csv', 'w+')
        csvWriter = csv.writer(csvFile)
        print("crawler training text data", end = "")
        count = 0
        tweets = self.get_tweet(extend, time, item)
        
        for tweet in tweets:
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
        print("\n")

    def crawler_test_text(self, extend, time, item):
        csvFile = open('input.test.text.csv', 'w+')
        csvWriter = csv.writer(csvFile)
        print("crawler testing text data", end = "")
        count = 0
        tweets = self.get_tweet(extend, time, item)

        for tweet in tweets:
            count = count + 1
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
        print("\n")

    def crawler_train_photo(self, time, item):
        csvFile = open('input.train.photo.csv', 'w+')
        csvWriter = csv.writer(csvFile)
        print("crawler training photo data", end="")
        count = 0
        tweets = self.get_tweet(False, time, item)

        for tweet in tweets:
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
                continue # filter out non-media tweet
                
            str_tag = ""
            if(tweet.entities['hashtags']):
                for item in tweet.entities['hashtags']:
                    if not judge_pure_english(item['text']):
                        continue
                    str_tag = str_tag + ', ' + item['text']
                str_tag = str_tag.replace(', ', '', 1)
            if(str_tag):
                csvWriter.writerow([str_photo, str_tag])
        print("\n")

    def crawler_test_photo(self, time, item):
        csvFile = open('input.test.photo.csv', 'w+')
        csvWriter = csv.writer(csvFile)
        print("crawler testing photo data", end="")
        count = 0
        tweets = self.get_tweet(False, time, item)

        for tweet in tweets:
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
        print("\n")

# if __name__ == '__main__':
#
#     tweet_crawler = TweetCrawler(
#         consumer_key, consumer_secret, access_token, access_token_secret)
#     tweet_crawler.crawler_train_text(extend=False, time="2019-10-13", item=200)
#     tweet_crawler.crawler_test_text(extend=False, time="2019-10-13", item=200)
#     tweet_crawler.crawler_train_photo(time="2019-10-13", item=200)
#     tweet_crawler.crawler_test_photo(time="2019-10-13", item=200)
