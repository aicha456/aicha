import streamlit as st
import numpy as np
import pandas as pd
import os
from streamlit_lottie import st_lottie
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import arabic_reshaper
import matplotlib.pyplot as plt
import seaborn as sns
import tweepy
import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import plotly.graph_objects as go
import numpy as np
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display

import requests



st.set_page_config(
    page_title=" Dashboard",
    page_icon="📈",

)




def load_lottieurl(url: str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
def chart (level):
    plot_bgcolor = "rgb(14,17,23)"
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

#consumer_key = 'MlYcPT94qliDArDpwD7uy4jwt'
#consumer_secret = 'Im8r1N3bPi4k1K0MIGE2KB1NUo5KL6qMY2n5fiV32Zprx3N69s'
#access_token = '756327168-ZVzm0SKuoeEyxeYz4LJkG4IQZqEja4dHG0QJwHgu'
#access_token_secret = 'Uii0oZfdKru8PP3iT5uUdsznjOLU2A58acptCJZxDaqup'
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
  lottie_he = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_up3nxxtl.json")
  st_lottie(
            lottie_he,
            width=200,
            height=200
        )

  chart(45)
  #st.title('level three')
  st.success('level  three', icon="✅")
elif 100< b <400:
      lottie_he = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_bveyhj83.json")
      st_lottie(
            lottie_he,
            width=200,
            height=200
        )


else :
  print("no level ")
  st.title('no level ')
  chart(5)
#tweet_df_5min = tweets_df.groupby(pd.Grouper(key='Datetime', freq='1Min', convention='start')).size()
#fig, ax = plt.subplots()
#ax.plot(tweet_df_5min )
#st.line_chart(tweet_df_5min)


c=[]
for i in tweets_df['Followers']:
  if 0 <i <100 :
    i=100
    c.append(i)
  elif   100<i <500 :
    i=50
    c.append(i)
  elif 500<i <1000 :
   i=1000
   c.append(i)
  elif 1000<i <10000 :
   i=10000
   c.append(i)
  elif 10000<i <100000 :
   i=100000
   c.append(i)
  else :
    i=1000000
    c.append(i)
tweets_df['folo'] = np.array(c)

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


tab1, tab2 ,tab3= st.tabs(["Followers", "source",'folo'])

with tab1:
   st.header("the Followers")
   fig3 = px.pie(tweets_df["Followers"].value_counts().head(), values=tweets_df["Followers"].value_counts().head().values, names=tweets_df["Followers"].value_counts().head().index, title='Followers')
   st.plotly_chart(fig3)

with tab2:
    st.header("the source")
    fig2 = px.pie(a, values=a.values, names=a.index, title='the source')
    #st.pyplot(fig)
    st.plotly_chart(fig2)

with tab3:


   fig4 = px.pie(tweets_df["folo"].value_counts().values, values=tweets_df["folo"].value_counts().values, names=['[0<Followers<100]','[100<Followers<500]','[500<Followers<1K]','[1K<Followers<10K]','[10K<Followers<100K]','[more then 100K]'], title='Followers')
   
   st.plotly_chart(fig4)

#Api = tweepy.API(auth)



import folium
import  geopy
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


#geo_locator = Nominatim(user_agent="LearnPython")
#m = folium.Map(location=[0, 0], zoom_start=2)
#f#or (name, location) in location_data:
        #if location:
            #try:
                ##location = geo_locator.geocode(location)
            #except GeocoderTimedOut:
                #continue
            #if location:
                #folium.Marker([location.latitude, location.longitude], popup=name).add_to(m)

#m = folium.Map(location=[0, 0], zoom_start=2)

    #st.map(map.save("index.html"))
consumer_key1 = 'MlYcPT94qliDArDpwD7uy4jwt'
consumer_secret1 = 'Im8r1N3bPi4k1K0MIGE2KB1NUo5KL6qMY2n5fiV32Zprx3N69s'
access_token1 = '756327168-ZVzm0SKuoeEyxeYz4LJkG4IQZqEja4dHG0QJwHgu'
access_token_secret1 = 'Uii0oZfdKru8PP3iT5uUdsznjOLU2A58acptCJZxDaqup'
#Authenticate with credentials
auth = tweepy.OAuthHandler(consumer_key1, consumer_secret1)
auth.set_access_token(access_token1, access_token_secret1)
apii = tweepy.API(auth)
def get_tweets(key_word):
    #Api = tweepy.API(auth)
    location_data = []
    for tweet in tweepy.Cursor(apii.search_tweets, q=key_word,lang = 'ar').items(100):
        if hasattr(tweet, 'user') and hasattr(tweet.user, 'screen_name') and hasattr(tweet.user, 'location'):
            if tweet.user.location:
                location_data.append((tweet.user.screen_name, tweet.user.location))
    return location_data


def removeWeirdChars(text):
    weirdPatterns = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u'\U00010000-\U0010ffff'
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               u"\u2069"
                               u"\u2066"
                               u"\u200c"
                               u"\u2068"
                               u"\u2067"
                               "]+", flags=re.UNICODE)
    return weirdPatterns.sub(r'', text)
tweets_loc = get_tweets(key_word)

plt.style.use('ggplot')
c='السعودية'
m='المملكة'
s='Saudi'
#a=tweets_df[0]
#if c in a[1]:
   #print('yes')
a=[]
d=[]
x=[]

for i in tweets_loc:
  b=i[1]
  if c in i[1]:
    a.append('السعودية')
  elif m  in i[1]:
    a.append('السعودية')
  elif s in  i[1]:
    a.append('السعودية')
  else:
   a.append(b)

D=Counter(a)
df =pd.DataFrame.from_dict(D, orient='index').reset_index()

common_element = D.most_common(10)



for i in df['index']:
  
  #o=get_display(arabic_reshaper.reshape(i))
  o=removeWeirdChars(i)
  x.append(o)

import plotly.figure_factory as ff

df['index'] = x
print(df['index'])
plt.figure(figsize = (20, 10))
df=df.sort_values(by=0,ascending=False)

df=df.head(30)
fig5 = px.bar(
      x= df['index'] , y=df[0])
#fig5=plt.bar(df['index'],df[0])

st.plotly_chart(fig5)




from streamlit_folium import folium_static
#m = folium.Map(location=[45.5236, -122.6750])
#folium_static(m)
if st.button('show me the map'):  
  

  data=get_tweets(key_word)
  m= folium.Map(location=[0, 0], zoom_start=2)
  #st.map(data)
  geo_locator = Nominatim(user_agent="LearnPython")
  for (name, location) in data:
        if location:
            try:
                location = geo_locator.geocode(location)
            except GeocoderTimedOut:
                continue
            if location:
                folium.Marker([location.latitude, location.longitude], popup=name).add_to(m)


  location_data = get_tweets(key_word)
  folium_static(m)    
  
