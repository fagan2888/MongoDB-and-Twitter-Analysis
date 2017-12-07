# -*- coding: utf-8 -*-

# Created by Zuoqi Zhang on 2017/12/5.

from pymongo import MongoClient
from textblob import TextBlob

client = MongoClient('localhost', 27017)
db = client.twitterdb
tweets = db.twitter_search

# print 'Number of tweets in the database:', tweets.count()

# A) Find the number of tweets that have data somewhere in the tweet's text (case insensitive search using regex)
related_tweets = tweets.find({'text': {'$regex': '.*data.*', '$options': 'i'}})
print 'Number of tweets that have \'data\' somewhere in the tweet\'s text:', related_tweets.count()

# print the created time, user's name, and text of each tweet.
# for tweet in related_tweets:
#     print 'created_at:', tweet['created_at']
#     print 'user.name:', tweet['user']['name']
#     print tweet['text'], '\n'

# B) From all the data related objects, how many of them are geo_enabled?
geo_enabled_tweets = tweets.find({'text': {'$regex': '.*data.*', '$options': 'i'}, 'user.geo_enabled': True})
print 'Number of geo_enabled tweets:', geo_enabled_tweets.count()

# print the created time, user's name, value of geo_enabled, and text of each tweet.
# for tweet in geo_enabled_tweets:
#     print 'created_at:', tweet['created_at']
#     print 'user.name:', tweet['user']['name']
#     print 'geo_enabled:', tweet['user']['geo_enabled']
#     print tweet['text'], '\n'

# C) For all the data related tweets, use the TextBlob Python library to detect if the Tweet’s sentiment is "Positive",
# "Neutral", or "Negative".
for tweet in related_tweets:
    text = TextBlob(tweet['text'])
    score = text.sentiment.polarity
    if score > 0:
        print 'postive sentiment for the tweet:', tweet['text']
    elif score < 0:
        print 'negative sentiment for the tweet:', tweet['text']
    else:
        print 'neutral sentiment for the tweet:', tweet['text']