# -*- coding: utf-8 -*-

# Created by Zuoqi Zhang on 2017/12/5.

from pymongo import MongoClient
from collections import OrderedDict
import re
import emoji
import folium

client = MongoClient('localhost', 27017)
db = client.usa_db
tweets = db.usa_tweets_collection

print('Number of tweets in the database:', tweets.count())

# set the starting coordinates and zoom level
tweet_map = folium.Map(location=[39.8333333, -98.585522], zoom_start=5) # a map of all tweets
emoji_map = folium.Map(location=[39.8333333, -98.585522], zoom_start=5) # a map of top 2 emojis of each state

all_states = [] # save the abbreviation of each state
state_coor = [] # choose a coordinate for each state
emoji_per_state = [] # count the number of emojis for each state
cnt = 0 # no. of current tweet

print('Creating two maps...')
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
        coor = tweet['geo']['coordinates']
        # Each state will be assigned a number which is the index of it in the following three arrays.
        # For instance, if Illinois is assigned 1, then
        # all_states[1] = 'IL',
        # state_coor[1] will be the coordinate of some place in IL,
        # emoji_per_state[1] will count the number of occurrence of each emoji in IL.
        if state not in all_states:
            all_states.append(state)
            state_coor.append(coor)
            emoji_per_state.append({})
        pos = all_states.index(state)
        for ch in text:
            if ch in emoji.UNICODE_EMOJI:
                if ch not in emoji_per_state[pos].keys():
                    emoji_per_state[pos][ch] = 1
                else:
                    emoji_per_state[pos][ch] += 1
        # draw a circle marker on the map for this tweet
        folium.CircleMarker(location=coor, radius=3).add_to(tweet_map)
        cnt += 1
        print(cnt, coor)
tweet_map.save('map.html')

# draw the map of emojis
for i in range(len(emoji_per_state)):
    emoji_count = OrderedDict(sorted(emoji_per_state[i].items(), key=lambda x: x[1], reverse=True))  # sort the dict by values, in descending order
    cnt = 0
    info = all_states[i]
    for k, v in emoji_count.items():
        info += ' ' + k + ': ' + str(v)
        cnt += 1
        if cnt == 2:
            break
    # For each state, draw a red icon on the map, and if you click on it, you will see the top 2 emojis in this state.
    folium.Marker(
        location=state_coor[i],
        popup=info,
        icon=folium.Icon(color='red')
    ).add_to(emoji_map)
emoji_map.save('emoji_of_state.html')

print('Two maps have been created.')