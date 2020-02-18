import os
import tweepy as tw
import pandas as pd
import csv


class TweetCrawler:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.auth = tw.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)

    def crawler_train(self, extend, time, item):
        csvFile = open('input.train.csv', 'w+')
        csvWriter = csv.writer(csvFile)
        print("start to crawler training data...")
        if (extend == False):
            for tweet in tw.Cursor(self.api.search, q="*",
                                   lang="en",
                                   since=time,
                                   ).items(item):
                #print (tweet.created_at, tweet.text)
                str = ""
                #print(tweet.text)
                if(tweet.entities['hashtags']):
                    for item in tweet.entities['hashtags']:
                        if not item['text'].isalnum():
                            continue
                    #print(item['text'])
                        str = str + ', ' + item['text']
                    str = str.replace(', ', '', 1)
                #print(tweet)
                if(("RT" not in tweet.text) and (str)):
                    csvWriter.writerow([tweet.text, str])


        else:
            for tweet in tw.Cursor(self.api.search, q="*",
                                   lang="en",
                                   since=time,
                                   tweet_mode="extended"
                                   ).items(item):
                #print (tweet.created_at, tweet.text)
                str = ""
                #print(tweet.text)
                if(tweet.entities['hashtags']):
                    for item in tweet.entities['hashtags']:
                        if not item['text'].isalnum():
                            continue
                        #print(item['text'])
                        str = str + ', ' + item['text']
                    str = str.replace(', ', '', 1)
                #print(tweet)
                if(("RT" not in tweet.full_text) and (str)):
                    csvWriter.writerow([tweet.full_text, str])
        print("finish to crawler training data!")

    def crawler_test(self, extend, time, item):
        csvFile = open('input.test.csv', 'w+')
        csvWriter = csv.writer(csvFile)
        print("start to crawler testing data...")
        if (extend == False):
            for tweet in tw.Cursor(self.api.search, q="*",
                                   lang="en",
                                   since=time,
                                   ).items(item):
                #print (tweet.created_at, tweet.text)
                str = ""
                #print(tweet.text)
                if(tweet.entities['hashtags']):
                    for item in tweet.entities['hashtags']:
                        if not item['text'].isalnum():
                            continue
                        #print(item['text'])
                        str = str + ', ' + item['text']
                    str = str.replace(', ', '', 1)
                #print(tweet)
                if("RT" not in tweet.text and not(str)):
                    csvWriter.writerow([tweet.text, str])

        else:
            for tweet in tw.Cursor(self.api.search, q="*",
                                   lang="en",
                                   since=time,
                                   tweet_mode="extended"
                                   ).items(item):
                #print (tweet.created_at, tweet.text)
                str = ""
                #print(tweet.text)
                if(tweet.entities['hashtags']):
                    for item in tweet.entities['hashtags']:
                        if not item['text'].isalnum():
                            continue
                        #print(item['text'])
                        str = str + ', ' + item['text']
                    str = str.replace(', ', '', 1)
                #print(tweet)
                if("RT" not in tweet.text and not(str)):
                    csvWriter.writerow([tweet.full_text, str])
        print("finish to crawler testing data!")

if __name__ == '__main__':

    tweet_crawler = TweetCrawler(
        consumer_key, consumer_secret, access_token, access_token_secret)
    tweet_crawler.crawler_train(extend=True, time="2019-10-13", item=500)
    tweet_crawler.crawler_test(extend=False, time="2019-10-13", item=200)
    dat = pd.read_csv('input.train.csv',
                      header=0, names=['text', 'tag'])
    dat.head()
