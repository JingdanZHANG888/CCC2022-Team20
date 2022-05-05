#!/usr/bin/env python
# coding: utf-8

# # 1. Twitter Analysis

# In[52]:


import couchdb
import pandas as pd
import matplotlib.pyplot as plt # 3.4.3
import json
from wordcloud import WordCloud, STOPWORDS # 1.8.1
from PIL import Image # 1.5.33
import numpy as np # 1.20.3
import re # 2021.8.3
import os
import requests, zipfile, io
import geopandas as gpd # 0.10.2
import folium # 0.12.1


# In[53]:


NSW_LAT = 151.081746
NSW_LNG = -33.932931
ZOOM = 10
VIC_LAT = 144.58
VIC_LNG = -37.60


# In[54]:


url = "http://172.26.131.170:5984"
user = "admin"
password = '170645'

server = couchdb.Server(url)
server.resource.credentials = (user, password)


# ### 1.1 Sentiment Propertions Analysis

# In[55]:


# Get Map Reduce result from Couchdb
db_mel = server["twitter_sentiment"]
view_mel = db_mel.view('sentiment_analysis/count_sentiment',group=True)

db_syd = server["twitter_sentiment_syd"]
view_syd = db_syd.view('sentiment_analysis/count_sentiment',group=True)


# In[56]:


# Get the results and store into csv
view_mel_df = pd.DataFrame()
mel_sentiment_type_list = []
mel_sentiment_count_list = []
mel_percentage_list = []
for row in view_mel:
    mel_sentiment_type_list.append(row.key)
    mel_sentiment_count_list.append(row.value)
for i in mel_sentiment_count_list:
    percentage = i / sum(mel_sentiment_count_list)
    mel_percentage_list.append(percentage)
view_mel_df['sentiment'] = mel_sentiment_type_list
view_mel_df['count'] = mel_sentiment_count_list
view_mel_df['percentage'] = mel_percentage_list

view_syd_df = pd.DataFrame()
syd_sentiment_type_list = []
syd_sentiment_count_list = []
syd_percentage_list = []
for row in view_syd:
    syd_sentiment_type_list.append(row.key)
    syd_sentiment_count_list.append(row.value)
for i in syd_sentiment_count_list:
    percentage = i / sum(syd_sentiment_count_list)
    syd_percentage_list.append(percentage)
view_syd_df['sentiment'] = syd_sentiment_type_list
view_syd_df['count'] = syd_sentiment_count_list
view_syd_df['percentage'] = syd_percentage_list


# In[57]:


# Pie chart
# colors
colors_mel = ['#ff9999','#66b3ff','#99ff99']
colors_syd = ['#c2c2f0','#ffb3e6','#ffcc99']

# explsion
explode = (0.05,0.05,0.05)

# Draw pie charts
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(10,5))

ax1.pie(mel_percentage_list, colors = colors_mel, labels=mel_sentiment_type_list, autopct='%1.1f%%', 
        startangle=90, pctdistance=0.85, explode = explode)
ax1.set_title('Tweets Sentiment Proportion in Melbourne')

ax2.pie(syd_percentage_list, colors = colors_syd, labels=syd_sentiment_type_list, autopct='%1.1f%%', 
        startangle=90, pctdistance=0.85, explode = explode)
ax2.set_title('Tweets Sentiment Proportion in Sydney')
fig.savefig('./Web/public/images/tweets_sentiment_piechart.png')
plt.tight_layout()
plt.show()


# ### 1.2 Word Cloud

# In[58]:


#Function to Create Wordcloud
def create_wordcloud(text, save_name):
    mask = np.array(Image.open("./data/cloud.png"))
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",
    mask = mask,
    max_words=3000,
    stopwords=stopwords,
    repeat=True)
    wc.generate(str(text))
    wc.to_file('./Web/public/images/' + save_name)
    print("Word Cloud Saved Successfully")
    path='./Web/public/images/' + save_name
    #display(Image.open(path))


# In[61]:


# export dataset from Couchdb
os.system('curl -X GET http://admin:170645@172.26.131.170:5984/twitter_sentiment/_all_docs\?include_docs\=true >           ./data/twitter_sentiment_mel.json')
os.system('curl -X GET http://admin:170645@172.26.131.170:5984/twitter_sentiment_syd/_all_docs\?include_docs\=true >           ./data/twitter_sentiment_syd.json')

# Read data
mel_file = open('./data/twitter_sentiment_mel.json')
twitter_mel = json.load(mel_file)
syd_file = open('./data/twitter_sentiment_syd.json')
twitter_syd = json.load(syd_file)


# In[62]:


# Create Melbourne word cloud
mel_list = []
for index, item in enumerate(twitter_mel['rows'][:-1]):
    content = item['doc']['content'].replace("https",'').split("://")[0]
    content = content.replace("will",'')
    content = content.replace("people",'')
    content = content.replace("one",'')
    content = re.sub("(@[A-Za-z0–9]+)"," ", content)
    content = re.sub('RT @\w+: '," ", content)
    mel_list.append(content)

create_wordcloud(mel_list, 'mel_wordcloud.png')

# Create Sydney word cloud
syd_text = []
for i in twitter_syd['rows'][:-1]:
    content = i['doc']['content'].replace("https",'').split("://")[0]
    content = content.replace("will",'')
    content = content.replace("people",'')
    content = content.replace("one",'')
    content = re.sub("(@[A-Za-z0–9]+)"," ", content)
    content = re.sub('RT @\w+: '," ", content)
    syd_text.append(content)

create_wordcloud(syd_text, 'syd_wordcloud.png')


# # 2. Aurin Data

# In[27]:


# Export AURIN Date from Couchdb
os.system('curl -X GET http://admin:170645@172.26.131.170:5984/income_2014/_all_docs\?include_docs\=true >           ./data/income.json')
os.system('curl -X GET http://admin:170645@172.26.131.170:5984/housing_2014/_all_docs\?include_docs\=true >           ./data/housing.json')


# In[63]:


# Read data
housing_file = open('./data/housing.json')
housing = json.load(housing_file)
income_file = open('./data/income.json')
income = json.load(income_file)


# In[64]:


# AURIN Housing
housing_df = pd.DataFrame()
housing_averageprice = []
housing_sa22016pid = []
housing_state = []
housing_sa22016code5digit = []
housing_sa22016name = []
for row in housing['rows']:
    housing_averageprice.append(row['doc']['properties']['sold_both_auction_private_treaty_averageprice'])
    housing_sa22016pid.append(row['doc']['properties']['sa22016pid'])
    housing_state.append(row['doc']['properties']['state'])
    housing_sa22016code5digit.append(row['doc']['properties']['sa22016code5digit'])
    housing_sa22016name.append(row['doc']['properties']['sa22016name'])

housing_df['sa22016code5digit'] = housing_sa22016code5digit
housing_df['sa22016name'] = housing_sa22016name
housing_df['sa22016pid'] = housing_sa22016pid
housing_df['state'] = housing_state
housing_df['sold_both_auction_private_treaty_averageprice'] = housing_averageprice

# AURIN Income
income_df = pd.DataFrame()
income_sa2_name16 = []
income_sa2_code_2016 = []
income_sa2_5dig16 = []
income_mean_aud_2014_15 = []
for row in income['rows']:
    income_sa2_name16.append(row['doc']['properties']['sa2_name16'])
    income_sa2_code_2016.append(row['doc']['properties']['sa2_code_2016'])
    income_sa2_5dig16.append(row['doc']['properties']['sa2_5dig16'])
    income_mean_aud_2014_15.append(row['doc']['properties']['mean_aud_2014_15'])

income_df['sa2_name16'] = income_sa2_name16
income_df['sa2_code_2016'] = income_sa2_code_2016
income_df['sa2_5dig16'] = income_sa2_5dig16
income_df['mean_aud_2014_15'] = income_mean_aud_2014_15


# In[65]:


# Download SA2 shapefile from website
zip_file_url = 'https://www.abs.gov.au/AUSSTATS/subscriber.nsf/log?openagent&1270055001_sa2_2016_aust_shape.zip&1270.0.55.001&Data%20Cubes&A09309ACB3FA50B8CA257FED0013D420&0&July%202016&12.07.2016&Latest'
r = requests.get(zip_file_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("./data")


# ### 2.1 Bar charts for comparing house price/income using Aurin data

# In[66]:


house = housing_df.rename(columns={'sa22016code5digit':'sa2_5dig16'})
house['sa2_5dig16'] = house['sa2_5dig16'].astype('int')
income_df['sa2_5dig16'] = income_df['sa2_5dig16'].astype('int')
# preprocess data
pre_total = pd.merge(house,income_df,on='sa2_5dig16')
pre_melb = pre_total[pre_total['state']=='VIC']
# filter suburbs that belong to Great Melbourne
pre_melb = pre_melb[(pre_melb['sa2_5dig16'] < 21386) &(pre_melb['sa2_5dig16'] > 21104)]
pre_syd = pre_total[pre_total['state']=='NSW']
# filter suburbs that belong to Great Sydney
pre_syd = pre_syd[(pre_syd['sa2_5dig16'] < 11445) &(pre_syd['sa2_5dig16'] > 11297)]

# extract useful information and delete data with NAN value
melb_income_house = pre_melb[['state','sa2_5dig16','sa2_name16','sold_both_auction_private_treaty_averageprice','mean_aud_2014_15']]
melb_income_house = melb_income_house.dropna()
melb_price_sum= sum(melb_income_house['sold_both_auction_private_treaty_averageprice'])
melb_income_sum = sum(melb_income_house['mean_aud_2014_15'])
melb_average = melb_price_sum/melb_income_sum

syd_income_house = pre_syd[['state','sa2_5dig16','sa2_name16','sold_both_auction_private_treaty_averageprice','mean_aud_2014_15']]
syd_income_house = syd_income_house.dropna()
syd_price_sum= sum(syd_income_house['sold_both_auction_private_treaty_averageprice'])
syd_income_sum = sum(syd_income_house['mean_aud_2014_15'])
syd_average = syd_price_sum/syd_income_sum


# In[72]:


# draw comparison of house price/income value between Melbourne and Sydney 

comparison_x = ['Melbourne','Sydney']
comparison_y = [melb_average,syd_average]

plt.figure(figsize=(10,6))
plt.bar(comparison_x,comparison_y, color ='maroon', width = 0.4)
plt.title('Comparison of house price/income value between Melbourne and Sydney',fontsize=18)

plt.savefig('./Web/public/images/Comparison.png',dpi=300)


# In[68]:


# Bar charts for comparing house price/income for suburbs in Melbourne and Sydney

# Plot for melbourne
melb_income_house['the rate of housing price and income'] = melb_income_house['sold_both_auction_private_treaty_averageprice']/melb_income_house['mean_aud_2014_15']
# Sort the 10 smallest rates
melb_income_house.sort_values(by='the rate of housing price and income',axis=0,ascending=True,inplace=True)
melb_top10 = melb_income_house[0:10]
melb_top10 = melb_top10[['sa2_name16','the rate of housing price and income']]

melb_x = melb_top10['sa2_name16']
melb_y = melb_top10['the rate of housing price and income']

melb_x_list = melb_top10['sa2_name16'].to_list()
melb_y_list = melb_top10['the rate of housing price and income'].to_list()
melb_y_list = list(np.around(np.array(melb_y_list),2))

plt.figure(figsize=(18,5))
plt.bar(melb_x, melb_y, width = 0.4)

for i in range(len(melb_y_list)):
    plt.annotate(str(melb_y_list[i]), xy=(melb_x_list[i],melb_y_list[i]), ha='center', va='bottom')
    
plt.title('10 suburbs in Melbourne with the smallest rate of house price and income',fontsize=18)
melb_label = [re.sub("(.{16})", "\\1\n", label, 0, re.DOTALL) for label in melb_x]
plt.xticks(range(10), melb_label)
plt.savefig('./Web/public/images/Melbourne.png',dpi=300)


# In[69]:


# Plot for Sydney
syd_income_house['the rate of housing price and income'] = syd_income_house['sold_both_auction_private_treaty_averageprice']/syd_income_house['mean_aud_2014_15']
# Sort the 10 smallest rates
syd_income_house.sort_values(by='the rate of housing price and income',axis=0,ascending=True,inplace=True)
syd_top10 = syd_income_house[0:10]
syd_top10 = syd_top10[['sa2_name16','the rate of housing price and income']]

syd_x = syd_top10['sa2_name16']
syd_y = syd_top10['the rate of housing price and income']

syd_x_list = syd_top10['sa2_name16'].to_list()
syd_y_list = syd_top10['the rate of housing price and income'].to_list()
syd_y_list = list(np.around(np.array(syd_y_list),2))

plt.figure(figsize=(18,5))
plt.bar(syd_x, syd_y, width = 0.4)

for i in range(len(syd_y_list)):
    plt.annotate(str(syd_y_list[i]), xy=(syd_x_list[i],syd_y_list[i]), ha='center', va='bottom')

plt.title('10 suburbs in Sydney with the smallest rate of house price and income',fontsize=18)
syd_label = [re.sub("(.{16})", "\\1\n", label, 0, re.DOTALL) for label in syd_x]
plt.xticks(range(10), syd_label)
plt.savefig('./Web/public/images/Sydney.png',dpi=300)


# ### 2.2 Map of housing price/income using Aurin data

# In[70]:


sf = gpd.read_file("./data/SA2_2016_AUST.shp")
sf['geometry'] = sf['geometry'].to_crs("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

nsw = housing_df[housing_df['state'] == 'NSW']
vic = housing_df[housing_df['state'] == 'VIC']
nsw_hi = pd.merge(nsw, income_df, left_on='sa22016name', right_on='sa2_name16').dropna()
vic_hi = pd.merge(vic, income_df, left_on='sa22016name', right_on='sa2_name16').dropna()

nsw_hi['mean'] = nsw_hi['sold_both_auction_private_treaty_averageprice'] / nsw_hi['mean_aud_2014_15']
vic_hi['mean'] = vic_hi['sold_both_auction_private_treaty_averageprice'] / vic_hi['mean_aud_2014_15']

sf['sa2'] = sf['SA2_MAIN16'].astype('str')
nsw_hi['sa2_code_2016'] = nsw_hi['sa2_code_2016'].astype('str')
vic_hi['sa2_code_2016'] = vic_hi['sa2_code_2016'].astype('str')

gdf_nsw = gpd.GeoDataFrame(pd.merge(nsw_hi, sf, left_on='sa2_code_2016', right_on='sa2')).drop('sa2_code_2016',axis=1)
gdf_vic = gpd.GeoDataFrame(pd.merge(vic_hi, sf, left_on='sa2_code_2016', right_on='sa2')).drop('sa2_code_2016',axis=1)

geoJSON_nsw = gdf_nsw[['SA2_MAIN16','geometry']].to_json()
geoJSON_vic = gdf_vic[['SA2_MAIN16','geometry']].to_json()


# In[71]:


# This code can be run locally but the file will be too large to upload.
# Draw population distribution
mean_nsw = folium.Map(location=[NSW_LNG, NSW_LAT], tiles="Stamen Terrain", zoom_start=ZOOM)

folium.Choropleth(
    geo_data=geoJSON_nsw, # geoJSON 
    name='choropleth', # name of plot
    data=gdf_nsw, # data source
    columns=['SA2_MAIN16','mean'], # the columns required
    key_on='properties.SA2_MAIN16', # this is from the geoJSON's properties
    fill_color='OrRd', # color scheme
    fill_opacity=0.9,
    line_opacity=0.5,
    legend_name='the rate of housing price and income' # legend title
).add_to(mean_nsw)

mean_nsw.save('./Web/public/images/mean_nsw.html')
#mean_nsw


# In[73]:


mean_vic = folium.Map(location=[VIC_LNG, VIC_LAT], tiles="Stamen Terrain", zoom_start=8)

folium.Choropleth(
    geo_data=geoJSON_vic, # geoJSON 
    name='choropleth', # name of plot
    data=gdf_vic, # data source
    columns=['SA2_MAIN16','mean'], # the columns required
    key_on='properties.SA2_MAIN16', # this is from the geoJSON's properties
    fill_color='OrRd', # color scheme
    fill_opacity=0.9,
    line_opacity=0.5,
    legend_name='the rate of housing price and income' # legend title
).add_to(mean_vic)

mean_vic.save('./Web/public/images/mean_vic.html')
#mean_vic


# In[ ]:




