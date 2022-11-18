import streamlit as st
import numpy as np
import pandas as pd
import os

import plotly.express as px
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import seaborn as sns
import tweepy
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
import numpy as np



st.set_page_config(
    page_title=" Dashboard",
    page_icon="📈",
    
)
def chart (level):
    plot_bgcolor = "White"
    quadrant_colors = [plot_bgcolor, "#f25829", "#f2a529", "#eff229", "#85e043"] 
    quadrant_text = ["", "<b>level three</b>", "<b>level two </b>", "<b>level one </b>", "<b>Very low</b>"]
    n_quadrants = len(quadrant_colors) - 1

    current_value = level
    min_value = 0
    max_value = 50
    hand_length = np.sqrt(2) / 4
    hand_angle = np.pi * (1 - (max(min_value, min(max_value, current_value)) - min_value) / (max_value - min_value))

    fig = go.Figure(
        data=[
        go.Pie(
            values=[0.5] + (np.ones(n_quadrants) / 2 / n_quadrants).tolist(),
            rotation=90,
            hole=0.5,
            marker_colors=quadrant_colors,
            text=quadrant_text,
            textinfo="text",
            hoverinfo="skip",
        ),
    ],
    layout=go.Layout(
        showlegend=False,
        margin=dict(b=0,t=10,l=10,r=10),
        width=450,
        height=450,
        paper_bgcolor=plot_bgcolor,
        annotations=[
            go.layout.Annotation(
                text=f"<b>the tweet level score of the tweet </b><br>",
                x=0.5, xanchor="center", xref="paper",
                y=0.25, yanchor="bottom", yref="paper",
                showarrow=False,
            )
        ],
        shapes=[
            go.layout.Shape(
                type="circle",
                x0=0.48, x1=0.52,
                y0=0.48, y1=0.52,
                fillcolor="#333",
                line_color="#333",
            ),
            go.layout.Shape(
                type="line",
                x0=0.5, x1=0.5 + hand_length * np.cos(hand_angle),
                y0=0.5, y1=0.5 + hand_length * np.sin(hand_angle),
                line=dict(color="#333", width=4)
            )
        ]
    )
)
    st.plotly_chart(fig)
#Twitter credentials
consumer_key = '78F6GWmlPoJX4CtW8E5A4dQYf'
consumer_secret = 'Uj3ZCkYe47HOLG0OOyXUly3wyvwhFAG8GLuQqZHVqse6VipfwJ'
access_token = '1310463220281495552-D8AOegt4AcMXgiC738DgD6STjQbaVi'
access_token_secret = 'PrcCzW7N4LmEcLIKnxv7VcX8ytwwCsAIdal2EWXROhKAh'
#Authenticate with credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
menu=['home','about']
choice = st.sidebar.selectbox("Menu",menu)
st.markdown("<h1 style='text-align: center; color: deepskyblue	;'>📉 key word anlaysis </h1>", unsafe_allow_html=True)

key_word = st.text_input('enter key word ', ' #')
st.write('The current keyword   is', key_word)
col1, col2 = st.columns([3, 3])

with col1:
    limit = st.slider(
        'Select a limit of tweets ',
        0, 1000 )
 

with col2:
    follower = st.slider(
        'Select a limit of follower ',
        0, 500 )
st.write('Values:', limit)


def TextClean(tweet):
    
    tweet = tweet.lower()
    tweet = re.sub(r'@[a-z0-9_]\S+', '', tweet)
    tweet = re.sub(r'#[a-z0-9_]\S+', '', tweet)
    tweet = re.sub(r'&[a-z0-9_]\S+', '', tweet)
    tweet = re.sub(r'[?!.+,;$%&"]+', '', tweet)
    tweet = re.sub(r'rt[\s]+', '', tweet)
    tweet = re.sub(r'\d+', '', tweet)
    tweet = re.sub(r'\$', '', tweet)
    tweet = re.sub(r'RT', '', tweet)
    return tweet
def tweet_search(key_word):
    i = 0
    tweets_df = pd.DataFrame(columns = ['Datetime','tweetID', 'Tweet', 'Username', 'Retweets', 'Followers','loc','source'])
    for tweet in tweepy.Cursor(api.search_tweets, q = key_word, count = 500, lang = 'ar').items():
        print('Tweets downloaded:', i, '/', limit, end = '\r')
        if tweet.user.followers_count > follower:
            tweets_df = tweets_df.append({'Datetime': tweet.created_at, 
                                          'tweetID': tweet.id,
                                          'Tweet': tweet.text, 
                                          'Username': tweet.user.screen_name, 
                                          'Retweets': tweet.retweet_count, 
                                          'Followers': tweet.user.followers_count,'loc':tweet.user.location,
                                          'source':tweet.source }, ignore_index = True
                                          )
            i += 1
        if i >= limit:
            break
        else:
            pass
        
    tweets_df['Datetime'] = pd.to_datetime(tweets_df['Datetime'], format = '%Y.%m.%d %H:%M:%S')    
    tweets_df.set_index('Datetime', inplace = False)
    #tweets_df.to_csv(key_word + '.csv', encoding = 'utf-8')
    tweets_df['CleanTweet'] = tweets_df['Tweet'].apply(TextClean)

    return tweets_df
tweets_df = tweet_search(key_word)

if st.button('show me dataset'):
    st.dataframe(tweets_df) 
a=tweets_df['source'].value_counts(normalize=True).mul(100).round(1)
print(a)
tweet_df_5min = tweets_df.groupby(pd.Grouper(key='Datetime', freq='1Min', convention='start')).size()
b=tweet_df_5min.max()
st.markdown("<h1 style=' text-align: center;color: red;'> Tweet level </h1>", unsafe_allow_html=True)

if 5 < b < 10 :
      print('level one')
      #st.title('tweet level')
      
      st.success('level one', icon="✅")
      chart(20)
elif 10 < b <20 :
  print('level two')
  
  #st.title('level ')
  st.success('level two', icon="✅")
  chart(30)
elif 20 < b < 100:
  print('level three')
  st.success('level  three', icon="✅")
  chart(50)
  #st.title('level three')
  st.success('level  three', icon="✅")

else :
  print("no level ")
  st.title('no level ')
  chart(5)
#tweet_df_5min = tweets_df.groupby(pd.Grouper(key='Datetime', freq='1Min', convention='start')).size()
#fig, ax = plt.subplots()
#ax.plot(tweet_df_5min )
#st.line_chart(tweet_df_5min)

st.markdown("<h1 style='text-align: center; color: deepskyblue;'>Tweet per minutes  </h1>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["min", "S"])

with tab1:
 tweet_df_5min = tweets_df.groupby(pd.Grouper(key='Datetime', freq='1Min', convention='start')).size()
 fig, ax = plt.subplots()
 ax.plot(tweet_df_5min )
 st.line_chart(tweet_df_5min)

with tab2:
    tweet_df_5min = tweets_df.groupby(pd.Grouper(key='Datetime', freq='1S', convention='start')).size()
    fig, ax = plt.subplots()
    ax.plot(tweet_df_5min )
    st.line_chart(tweet_df_5min)
  

#tweets_df['source'].value_counts().plot.pie()
a=tweets_df['source'].value_counts(normalize=True).mul(100).round(1)
print(a)
tweet_df_5min = tweets_df.groupby(pd.Grouper(key='Datetime', freq='1Min', convention='start')).size()
b=tweet_df_5min.max()





st.markdown("<h1 style='text-align: center; color: deepskyblue;'>Tweet Source and Followers</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([10, 3])

with col1:
   st.metric(label="max tweet in 1min", value=b, delta="tweet in 1Min")


with col2:
   st.metric(label="Followers av", value=tweets_df['Followers'].mean(), delta="tweet in 1Min")


tab1, tab2 = st.tabs(["Followers", "source"])

with tab1:
   st.header("the Followers")
   f=tweets_df["Followers"].value_counts().head()
   fig3 = px.pie(f, values=f.values, names=f.index, title='Followers')
   st.plotly_chart(fig3)

with tab2:
    st.header("the source")
    fig2 = px.pie(a, values=a.values, names=a.index, title='the source')
    #st.pyplot(fig)
    st.plotly_chart(fig2)



