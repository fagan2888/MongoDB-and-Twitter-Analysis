# -*- coding: utf-8 -*-

# Created by Zuoqi Zhang on 2017/12/5.

import re
from pymongo import MongoClient
from emoji import UNICODE_EMOJI
from collections import OrderedDict

client = MongoClient('localhost', 27017)
db = client.usa_db
tweets = db.usa_tweets_collection

print 'Number of tweets in the database:', tweets.count()

# B. Find the tweets that have at least one emoji in them.

print '\n -- Tweets that have at least one emoji --'

emoji_count = {} # key: emoji, value: number of occurrence of this emoji
emoji_in_MA = {} # key: emoji, value: number of occurrence of this emoji in MA
state_count = {} # key: state, value: number of occurrence of the 'Christmas tree' emoji in this state
emoji_used = {} # key: state, value: number of emojis used in this state
tweets_per_state = {} # key: state, value: number of tweets from this state
tweets_per_city = {} # key: city in California, value: number of tweets from this city

for tweet in tweets.find():
    text = tweet['text']
    place = tweet['place']
    if place is None: # In case some tweets do not have the 'place' attribute.
        continue
    full_name = place['full_name']
    # Use regular expression to match the pattern 'City, State'.
    # Strings like 'Boston, MA', 'New York, NY' will be matched.
    # Strings like 'Texas, USA', 'Toronto, Ontario' will not be matched.
    if re.search('^.+, [A-Z]{2}$', full_name) is not None:
        state = full_name[-2:]
        # update tweets_per_state
        if not tweets_per_state.has_key(state):
            tweets_per_state[state] = 1
        else:
            tweets_per_state[state] += 1
        # update tweets_per_city
        if state == 'CA':
            # split the string by the last comma
            # left: name of the city
            # right: abbreviation for the state
            city = str(full_name).rsplit(', ', 1)[0]
            if not tweets_per_city.has_key(city):
                tweets_per_city[city] = 1
            else:
                tweets_per_city[city] += 1
        flag = False # flag = True if a tweet has at least one emoji.
        for ch in text:
            if ch in UNICODE_EMOJI: # check if a character is an emoji
                flag = True
                # update emoji_count
                if not emoji_count.has_key(ch):
                    emoji_count[ch] = 1
                else:
                    emoji_count[ch] += 1
                # update emoji_in_MA
                if state == 'MA':
                    if not emoji_in_MA.has_key(ch):
                        emoji_in_MA[ch] = 1
                    else:
                        emoji_in_MA[ch] += 1
                # update state_count
                if ch == unicode('🎄', 'utf-8'): # convert the emoji to unicode
                    if not state_count.has_key(state):
                        state_count[state] = 1
                    else:
                        state_count[state] += 1
                # update emoji_used
                if not emoji_used.has_key(state):
                    emoji_used[state] = 1
                else:
                    emoji_used[state] += 1
        if flag:
            print text # print the text of a tweet

# 1. What are the top 15 emojis used in the entire tweets?

print '\n -- Top 15 emojis --'
emoji_count = OrderedDict(sorted(emoji_count.items(), key=lambda x: x[1], reverse=True)) # sort the dict by values, in descending order
cnt = 0
for k, v in emoji_count.items():
    print k, v
    cnt += 1
    if cnt == 15:
        break

# 2. What are the top 5 states for the emoji 🎄?

print '\n -- Top 5 states for 🎄 --'
state_count = OrderedDict(sorted(state_count.items(), key=lambda x: x[1], reverse=True)) # sort the dict by values, in descending order
cnt = 0
for k, v in state_count.items():
    print k, v
    cnt += 1
    if cnt == 5:
        break

# 3. What are the top 5 emojis for MA?

print '\n -- Top 5 emojis for MA --'
emoji_in_MA = OrderedDict(sorted(emoji_in_MA.items(), key=lambda x: x[1], reverse=True)) # sort the dict by values, in descending order
cnt = 0
for k, v in emoji_in_MA.items():
    print k, v
    cnt += 1
    if cnt == 5:
        break

# 4. What are the top 5 states that use emojis?

print '\n -- Top 5 states that use emojis --'
emoji_used = OrderedDict(sorted(emoji_used.items(), key=lambda x: x[1], reverse=True)) # sort the dict by values, in descending order
cnt = 0
for k, v in emoji_used.items():
    print k, v
    cnt += 1
    if cnt == 5:
        break

# C. Use MongoDB queries within PyMongo API to answer the following.

# 1. What are the top 5 states that have tweets?

print '\n -- Top 5 states that have tweets --'
tweets_per_state = OrderedDict(sorted(tweets_per_state.items(), key=lambda x: x[1], reverse=True)) # sort the dict by values, in descending order
cnt = 0
for k, v in tweets_per_state.items():
    print k, v
    cnt += 1
    if cnt == 5:
        break

# 2. In the state of California, what are the top 5 cities that tweet?

print '\n -- Top 5 cities in California that tweet --'
tweets_per_city = OrderedDict(sorted(tweets_per_city.items(), key=lambda x: x[1], reverse=True)) # sort the dict by values, in descending order
cnt = 0
for k, v in tweets_per_city.items():
    print k, v
    cnt += 1
    if cnt == 5:
        break