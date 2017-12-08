# -*- coding: utf-8 -*-

# Created by Zuoqi Zhang on 2017/12/7.

from pymongo import MongoClient
import csv
import os
import re
import folium

db = MongoClient().usa_db

# convert the database saved in MongoDB to csv format
if os.path.exists('usa_tweets.csv'):
    os.remove('usa_tweets.csv')

with open('usa_tweets.csv', 'w') as outfile:
    field_names = ['text', 'user', 'created_at', 'geo', 'location']
    writer = csv.DictWriter(outfile, delimiter=',', fieldnames=field_names)
    writer.writeheader()

    for data in db.usa_tweets_collection.find():
        # filter the tweets which are not in the 'XXXXXX, XX' format
        if data['place'] is None:
            continue
        if re.search('^.+, [A-Z]{2}$', data['place']['full_name']) is None:
            continue
        writer.writerow({
            # In case of the unicode encode error, here I add '.encode('utf-8')' to the original code.
            'text': data['text'].encode('utf-8'),
            'user': data['user']['name'].encode('utf-8'),
            'created_at': data['created_at'],
            'geo': data['geo']['coordinates'],
            'location': data['place']['full_name']
        })

    outfile.close()

# create a map of all the tweets
print 'Creating a map of all tweets...'
# set the starting coordinates and zoom level
tweet_map = folium.Map(location=[37.0902, -95.7129], zoom_start=5)
# read the output csv file again
with open('usa_tweets.csv', 'rb') as infile:
    csvreader = csv.reader(infile, delimiter=',')
    cnt = 0
    for row in csvreader:
        # The first row is 'text, user, created_at, geo, location' and does not contain any data.
        if cnt == 0:
            cnt += 1
            continue
        # row[3] is a string like '[42.0450722, -87.6876969]'.
        # extract latitude and longitude from this string
        coor = str(row[3]).replace('[', '').replace(']', '').split(', ')
        # draw a circle marker on the map
        folium.CircleMarker(location=[float(coor[0]), float(coor[1])], radius=3).add_to(tweet_map)
        cnt += 1
        print cnt, row[3]
        # if cnt == 1000:
        #     break
tweet_map.save('map.html')