import streamlit as st
import numpy as np
import pandas as pd
import os

import tweepy
import re

import time
import pywhatkit

import requests




st.set_page_config(
    page_title=" Dashboard",
    page_icon="📈",

)





#Twitter credentials
consumer_key = '78F6GWmlPoJX4CtW8E5A4dQYf'
consumer_secret = 'Uj3ZCkYe47HOLG0OOyXUly3wyvwhFAG8GLuQqZHVqse6VipfwJ'
access_token = '1310463220281495552-D8AOegt4AcMXgiC738DgD6STjQbaVi'
access_token_secret = 'PrcCzW7N4LmEcLIKnxv7VcX8ytwwCsAIdal2EWXROhKAh'

#consumer_key = 'MlYcPT94qliDArDpwD7uy4jwt'
#consumer_secret = 'Im8r1N3bPi4k1K0MIGE2KB1NUo5KL6qMY2n5fiV32Zprx3N69s'
#access_token = '756327168-ZVzm0SKuoeEyxeYz4LJkG4IQZqEja4dHG0QJwHgu'
#access_token_secret = 'Uii0oZfdKru8PP3iT5uUdsznjOLU2A58acptCJZxDaqup'
#Authenticate with credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
menu=['serch by key_word','serch by username']
choice = st.sidebar.selectbox("Menu",menu)
if choice == "serch by key_word":
 st.markdown("<h1 style='text-align: center; color: deepskyblue	;'>📉 key word anlaysis </h1>", unsafe_allow_html=True)

 key_word = st.text_input('enter key word ', ' #')
 st.write('The current keyword   is', key_word)

 



def track():
 def tweet_search(key_word):
    i = 0
    tweets_df = pd.DataFrame(columns = ['Datetime','tweetID', 'Tweet', 'Username', 'Retweets', 'Followers','loc','source'])
    for tweet in tweepy.Cursor(api.search_tweets, q = key_word, count = 500, lang = 'ar').items():
        print('Tweets downloaded:', i, '/', 100, end = '\r')
        if tweet.user.followers_count > 0:
            tweets_df = tweets_df.append({'Datetime': tweet.created_at, 
                                          'tweetID': tweet.id,
                                          'Tweet': tweet.text, 
                                          'Username': tweet.user.screen_name, 
                                          'Retweets': tweet.retweet_count, 
                                          'Followers': tweet.user.followers_count,'loc':tweet.user.location,
                                          'source':tweet.source }, ignore_index = True
                                          )
            i += 1
        if i >= 100:
            break
        else:
            pass
        
    tweets_df['Datetime'] = pd.to_datetime(tweets_df['Datetime'], format = '%Y.%m.%d %H:%M:%S')    
    tweets_df.set_index('Datetime', inplace = False)
    #tweets_df.to_csv(key_word + '.csv', encoding = 'utf-8')
    #tweets_df['CleanTweet'] = tweets_df['Tweet'].apply(TextClean)

    return tweets_df
 tweets_df = tweet_search(key_word)

 if st.button('show me tweets'):
    st.dataframe(tweets_df[['tweetID','Tweet','Username','Followers','source']]) 
 a=tweets_df['source'].value_counts(normalize=True).mul(100).round(1)
 print(a)
 tweet_df_5min = tweets_df.groupby(pd.Grouper(key='Datetime', freq='1Min', convention='start')).size()
 b=tweet_df_5min.max()

 t=time.localtime()

  
  #st.title('level ')

 if 5 < b < 300 :
          t=time.localtime()
          h=int(t.tm_hour)
          



 pywhatkit.sendwhatmsg('+966 55 511 9335','level three',time_hour=h ,time_min=int(t.tm_min)+1
            ,wait_time=1,tab_close=True)





       
      

  #st.title('level three')




#track()
while(True):
    track()
    time.sleep(60)