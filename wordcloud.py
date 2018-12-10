#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 15:46:10 2018

@author: zihaoli
"""

import tweepy
import json
import sys
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS 
 
consumer_key = 'wHKeXtfLQkzhkdIMCuIE5WWgO'
consumer_secret = 'UCXcjs2jwD9IptoMOzDTj61w4j1dfzG9By0Ex1QE9IkZUDbq6n'
access_token = '912482222443257856-kqdM00gwZa0isB4XWokvMmEiz2xxBHg'
access_secret = '3LnLXojpV1JLlYa9QSLrRTMDEB2UTjzDahFCbBMeNOiwi'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

 
class MyListener(StreamListener):
    print("In Listener...")
    tweet_number = 0
    
    def __init__(self, max_tweets, rawfile):
        self.max_tweets = max_tweets
        print(self.max_tweets)
 
    def on_data(self, data):
        self.tweet_number+=1 
        #print("In on_data", self.tweet_number)
        try:
            #print("In on_data in try")
            tweet=json.loads(data)
            with open(rawfile, 'a') as f:
                    tweet_text=tweet["text"]
                    print(tweet_text,"\n")
                    f.write(tweet_text) # the text from the tweet
                    json.dump(tweet, f) # write the raw tweet
        except BaseException:
            print("NOPE")
            pass
        if self.tweet_number>=self.max_tweets:
            sys.exit('Limit of '+str(self.max_tweets)+' tweets reached.')
    #method for on_error()
    def on_error(self, status):
        print("ERROR")
        if(status==420):
            print("Error ", status, "rate limited")
            return False

num_of_tweet = eval(input("How many tweets do you want to get: "))
hash_tag = input("Enter the hash name, such as #stock: ")

if num_of_tweet > 50:
    num_of_tweet = eval(input("The number of tweets you want collect exceeds the limit, \nplease enter a value that is smaller than 30: "))
if (hash_tag[0] == "#"):
    without_hash_tag = hash_tag[1:]
else:
    hash_tag = input("Enter the hash name, starts with #: ")

#Create a file for tweetmining    
rawfile="tweets_"+without_hash_tag+".json"

twitter_stream = Stream(auth, MyListener(num_of_tweet, rawfile))
twitter_stream.filter(track=[hash_tag])


d = path.dirname(__file__)
Rawfilename="tweetsforwordcloud.txt"
text = open(path.join(d, Rawfilename)).read()
#print(text)


wordcloud = WordCloud(
        background_color='white',
        stopwords={"and", "And", "AND","THIS", "This", "this", "FOR", "For", "quoted_status_id", "quoted_status_id_str", "u00e0", "onda", "href", "ud83e", "id_str", "resize",
             "THE", "The", "the", "is", "IS", "Is", "or", "OR", "Or", "will", "u200d", "u2642", "quoted_status", "ud83c", "u00c9REA", "pouca", "urls", "udd", "Mão", "mp4",
             "Will", "WILL", "still", "Still", "Need", "need", "food", "Food", "ud83d", "quoted_status_permalink", "isn", "Não", "AÉREA", "screen_name", "false", "null",
             "porn", "dra", "But", "but", "Has", "has", "about", "with", "all", "I", "you", "your", "his", "her", "ud83c", "nofollow", "filter_level", "content_type", "udf",
             "ser", "its", "put", "just", "PureM", "beIN", "u0650", "u00f6", "u00f3", "u00edcias", "u00edculo", "u00c9REA", "tirou", "TweetDeck", "notifications", "com",
             "u2026", "u26bd", "timestamp_ms", "media_url", "media_url_https", "is_quote_status", "quote_count", "reply_count", "truncated", "retweeted_status", "u20e3",
             "followers_count", "retweet_count", "favorite_count", "follow_request_sent", "C0DFEC", "profile_text_color", "profile_use_background_image", "viu", "have",
             "profile_image_url", "profile_image_url_https", "profile_banner_url", "default_profile", "default_profile_image", "profile_sidebar_border_color", "for",
             "friends_count", "is_translator", "profile_background_color", "profile_background_image_url", "profile_background_image_url_https", "indices", "udc", 
             "listed_count", "url", "profile_background_tile", "profile_link_color", "profile_sidebar_border_color", "FFF", "contributors_enabled", "ufe", "pMr", 
             "statuses_count", "in_reply_to_status_id_str", "in_reply_to_user_id", "in_reply_to_user_id_str", "in_reply_to_screen_name", "user", "contributors",
             "display_text_range", "translator_type", "utc_offset", "hashtags", "place_type", "full_name", "country_code", "QUE", "ESTOU", "created_at", "text",
             "seguindoabatida", "Tapatio", "openinvitationpodcast", "u2764", "u2652", "IAM_ShayMyers", "u2019t", "CC0808", "udfc", "udde", "statuses_count",
             "source_user_id_str", "source_user_id", "source_status_id_str", "source_status_id", "embeddable", "expanded_url", "additional_media_info", "thus" 
             "user_mentions", "display_url", "profile_sidebar_fill_color", "in_reply_to_status_id", "favourites_count", "description",  "id_str", "though",
             "hwy", "C0DEED", "DDEEF", "bounding_box", "are", "video_info", "x-mpegURL", "You", "our", "EEE", "EFEFEF", "I'm", "weren't", "bitrate"},
        max_font_size=40, 
        scale=3,
    ).generate(text)

# Open a plot of the generated image.
plt.figure(num =1, figsize=(5, 5), dpi=120)
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('telcom_wordcloud.png')
