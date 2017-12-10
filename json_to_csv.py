# -*- coding: utf-8 -*-

# Created by Zuoqi Zhang on 2017/12/7.

from pymongo import MongoClient
import csv
import os
import re

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
            'text': data['text'],
            'user': data['user']['name'],
            'created_at': data['created_at'],
            'geo': data['geo']['coordinates'],
            'location': data['place']['full_name']
        })

    outfile.close()