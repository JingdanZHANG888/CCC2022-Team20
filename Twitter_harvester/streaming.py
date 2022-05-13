
# Part of COMP90024 Cluster and Cloud Computing from The University of Melbourne 
# Assignment 2 - Team 20
# Collective Team Details (Member's Name/Student ID/Location): 
#
#  * Cenxi Si 1052447 China
#  * Yipei Liu 1067990 China
#  * Jingdan Zhang 1054101 China
#  * Chengyan Dai 1054219 Melbourne
#  * Ruimin Sun 1052182 China



import tweepy
import json as js
import random
import sys

# read twitter keys
f1 = open('twitter_keys.json')
keys = js.load(f1)

api_key = keys["keys"][0]["detail"]["TWITTER_API_KEY"]
api_secret = keys["keys"][0]["detail"]["TWITTER_API_KEY_SECRET"]
access_token = keys["keys"][0]["detail"]["TWITTER_ACCESS_TOKEN"]
access_secret = keys["keys"][0]["detail"]["TWITTER_ACCESS_SECRET"]

#authentication
auth = tweepy.OAuth1UserHandler(api_key,api_secret)
auth.set_access_token(access_token,access_secret)
api = tweepy.API(auth)

# read real-time tweets

class Listener(tweepy.Stream):

    tweets = []
    limit = 100

    
    def on_status(self,status):
        self.tweets.append(status)

        if len(self.tweets) == self.limit:
            self.disconnect()

    def on_error(self,status_code):
        print(status_code)
        return False

    def on_timeout(self):
        print (sys.stderr, 'Timeout...')
        return False # Don't kill the stream


stream_tweet = Listener(api_key,api_secret,access_token,access_secret)


# read files
f2 = open('keywords.json')
keywords = js.load(f2)



# random get 30 current key words for searching
housing_words = random.choices(keywords['housing'], k=10)
income_words = random.choices(keywords['income'], k=10)
# convert these keywords into a string
def list_trans(targetlist):
    for i in range(len(targetlist)):
        targetlist[i] = 'the,'+targetlist[i]
    return targetlist


#stream by keywords
stream_keywords = list_trans(housing_words)+list_trans(income_words)

# melb-bounding-box
melb_bounding = [144.9514,-37.8231,144.9749,-37.8059]


#stream_tweet.filter(locations=melb_bounding)
stream_tweet.filter(track=stream_keywords)


jsontext = {'tweets':[]}

for tweet in stream_tweet.tweets:
    if 'RT' not in tweet.text:
        jsontext['tweets'].append({'id':tweet.id,'content':tweet.text,'coord':tweet.coordinates,
                                   'place':str(tweet.place),'user_location':tweet.user.location,
                                   'created_date':str(tweet.created_at.date())})



jsondata = js.dumps(jsontext, indent=4, separators=(',', ': '))

f = open('streamer_keywords.json', 'w')
f.write(jsondata)
f.close



