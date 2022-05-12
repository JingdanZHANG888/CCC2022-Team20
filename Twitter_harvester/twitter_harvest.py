#!/usr/bin/env python
# coding: utf-8

# ## Twitter Harvest

# Reference: \
# housing key words: https://www.wordstream.com/popular-keywords/real-estate-keywords?aliId=eyJpIjoiZXQwMHhlbHc5WTBEdksxSSIsInQiOiJiT01uUkVrY0M4eTFRSDh0ZWc2bG13PT0ifQ%253D%253D \
# income key words: https://www.thesaurus.com/browse/income

# In[3]:


import datetime
import time
import json
import random
import couchdb
import tweepy
import sys
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from operator import itemgetter

nltk.download('vader_lexicon')


# In[17]:


FMT = '%Y-%m-%d %H:%M:%S'
LIMIT_IN_SEC = 900
WAIT = 60
NOW = datetime.datetime.now().strftime(FMT)

url = "http://172.26.131.170:5984"
user = "admin"
password = '170645'

# Latitude and longitude coordinates
mel_geo = '-37.840935,144.946457,200km'
syd_geo = '-33.867487,151.206990,200km'


# In[19]:


# initialize twitter keys state
f1 = open('twitter_keys.json')
twitter_keys = json.load(f1)
current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
for i in range(4):
    twitter_keys["keys"][i]["last_used"] = '2022-04-10 00:00:00'
    twitter_keys["keys"][i]["flag"] = 'False'
a_file = open('twitter_keys.json', "w")
json.dump(twitter_keys, a_file)
a_file.close()

# read files
f2 = open('keywords.json')
keywords = json.load(f2)


# In[5]:


def random20_keywords(key_word_file):
    # random get 20 current key words for searching
    housing_words = random.choices(key_word_file['housing'], k=10)
    income_words = random.choices(key_word_file['income'], k=10)
    mel_words = random.choices(key_word_file['Melbourne'], k=10)
    # convert these keywords into a string
    only_housing = '" OR "'.join(housing_words)
    only_housing = '"' + only_housing + '"'
    only_income = '" OR "'.join(income_words)
    only_income = '"' + only_income + '"'
    income_housing = only_housing + ' OR ' + only_income
    mel_housing = '" OR "'.join(mel_words)
    mel_housing = only_housing + ' OR "' + mel_housing + '"'
    return income_housing


# In[12]:


def select_a_valid_twitter_key(twitter_keys_file, remove_key):
    f1 = open('twitter_keys.json')
    twitter_keys = json.load(f1)
    # get all valid twitter keys
    get_key = []
    duration_list = []
    rest_time = []
    # remove melbourne used key
    if remove_key != None:
        del twitter_keys["keys"][remove_key]
    while True:
        for valid_key in twitter_keys["keys"]:
            duration = datetime.datetime.now() - datetime.datetime.strptime(valid_key["last_used"], FMT)
            duration_in_s = duration.total_seconds()
            position = valid_key["id"] - 1
            rest_time.append(duration_in_s)
      
            if duration_in_s >= 900:
                get_key.append(valid_key)
                add_info = [duration_in_s, position]
                duration_list.append(add_info)
                
        # if there is no valid key to select, the system needs to wait
        if len(get_key) == 0:
            wait_time_in_s = LIMIT_IN_SEC - max(rest_time)
            print("Wait " + str(wait_time_in_s) + " seconds for Available Twitter key")
            time.sleep(wait_time_in_s)
            
        # if there is a valid key existing, we use the key which rests longest.
        else:
            duration_list.sort(key = itemgetter(0))
            index = duration_list[-1][1]
            print("Find a valid twitter key: ", index+1)
            # get twitter API
            consumer_key = get_key[index]["detail"]["TWITTER_API_KEY"]
            consumer_secret = get_key[index]["detail"]["TWITTER_API_KEY_SECRET"]
            bearer_token = get_key[index]["detail"]["TWITTER_BEARER_TOKEN"]
            access_token = get_key[index]["detail"]["TWITTER_ACCESS_TOKEN"]
            access_token_secret = get_key[index]["detail"]["TWITTER_ACCESS_SECRET"]
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
                
            return api, index


# In[7]:


def analysis_Twitter_Sentiment(text):
    sentiment = 0
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    neg = score['neg']
    neu = score['neu']
    pos = score['pos']
    if neg > pos:
        sentiment = 'negative'
    elif pos > neg:
        sentiment = 'positive'
    elif pos == neg:
        sentiment = 'neutral'
    return sentiment


# In[23]:


def harvest_tweets(tweets, dbname, key_position):
    for tweet in tweets:
            tweet_id = tweet.id
            tweet_text = tweet.text
            tweet_coord = tweet.coordinates
            tweet_place = tweet.place
            tweet_user_location = tweet.user.location
            tweet_Date = tweet.created_at.date()
            tweet_sentiment = analysis_Twitter_Sentiment(tweet_text)
            tweet_info = {'id': str(tweet_id), 
                          'content': tweet_text, 
                          'coordinates': tweet_coord, 
                          'place': str(tweet_place),
                          'user_location': tweet_user_location,
                          'created_date': str(tweet_Date),
                          'sentiment': tweet_sentiment
                         } 
    
            # add to Couchdb
            server = couchdb.Server(url)
            # Set credentials if necessary
            server.resource.credentials = (user, password)
            if dbname not in server:
                server.create(dbname)
            db = server[dbname]
            if str(tweet_info["id"]) not in db:
                tweet_info["_id"] = str(tweet_info["id"])
                db.save(tweet_info)
                print(tweet_info)
                print("Sucessfully saved to Couchdb:", dbname)
            
            # update last used time of current twitter key
            with open('twitter_keys.json', 'r') as f:
                update_key_state = json.load(f)
                keys = update_key_state['keys']
                keys[key_position]['last_used'] = datetime.datetime.now().strftime(FMT)

            with open('twitter_keys.json', 'w') as f:
                json.dump(update_key_state, f, indent=2)


# In[ ]:


# get twitter key
api, position = select_a_valid_twitter_key(twitter_keys, None)
api2, position2 = select_a_valid_twitter_key(twitter_keys, position)

# get query words
query = random20_keywords(keywords)

# get tweets
mel_tweets = tweepy.Cursor(api.search_tweets, q=query, geocode=mel_geo).items()
syd_tweets = tweepy.Cursor(api2.search_tweets, q=query, geocode=syd_geo).items()
while True:
    try:
        harvest_tweets(mel_tweets, "twitter_sentiment", position)
        harvest_tweets(syd_tweets, "twitter_sentiment_syd", position2)
        
    except tweepy.errors.TweepyException as e:
        print("Error: ", e)
        
        # update current twitter key's state and last used time
        with open('twitter_keys.json', 'r') as f:
            update_key_state = json.load(f)
            keys = update_key_state['keys']
            keys[position]['last_used'] = datetime.datetime.now().strftime(FMT)
            keys[position2]['last_used'] = datetime.datetime.now().strftime(FMT)

        with open('twitter_keys.json', 'w') as f:
            json.dump(update_key_state, f, indent=2)
        
        # begin a new twitter API
        query = random20_keywords(keywords)
        api, position = select_a_valid_twitter_key(twitter_keys, None)
        api2, position2 = select_a_valid_twitter_key(twitter_keys, position)
        mel_tweets = tweepy.Cursor(api.search_tweets, q=query, geocode=mel_geo).items()
        syd_tweets = tweepy.Cursor(api2.search_tweets, q=query, geocode=syd_geo).items()      
        
    except StopIteration:
        continue
    


# In[ ]:




