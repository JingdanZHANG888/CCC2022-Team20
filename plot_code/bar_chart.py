'''plot bar charts for comparing house price/income using Aurin data'''

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt

# read aurin data
house = pd.read_csv('../aurin_data/apm_sa2_2016_timeseries-585448897261193942.csv')
house = house.rename(columns={' sa22016code5digit':' sa2_5dig16'})
income = pd.read_csv('../aurin_data/abs_epi_employee_income_sa2_2010_15-6921393106736047504.csv')

# preprocess data
pre_total = pd.merge(house,income,on=' sa2_5dig16')
pre_melb = pre_total[pre_total[' state']=='VIC']
# filter suburbs that belong to Great Melbourne
pre_melb = pre_melb[(pre_melb[' sa2_5dig16'] < 21386) &(pre_melb[' sa2_5dig16'] > 21104)]
pre_syd = pre_total[pre_total[' state']=='NSW']
# filter suburbs that belong to Great Sydney
pre_syd = pre_syd[(pre_syd[' sa2_5dig16'] < 11445) &(pre_syd[' sa2_5dig16'] > 11297)]

# extract useful information and delete data with NAN value
melb_income_house = pre_melb[[' state',' sa2_5dig16','sa2_name16',' sold_both_auction_private_treaty_averageprice',' mean_aud_2014_15']]
melb_income_house = melb_income_house.dropna()
melb_price_sum= sum(melb_income_house[' sold_both_auction_private_treaty_averageprice'])
melb_income_sum = sum(melb_income_house[' mean_aud_2014_15'])
melb_average = melb_price_sum/melb_income_sum

syd_income_house = pre_syd[[' state',' sa2_5dig16','sa2_name16',' sold_both_auction_private_treaty_averageprice',' mean_aud_2014_15']]
syd_income_house = syd_income_house.dropna()
syd_price_sum= sum(syd_income_house[' sold_both_auction_private_treaty_averageprice'])
syd_income_sum = sum(syd_income_house[' mean_aud_2014_15'])
syd_average = syd_price_sum/syd_income_sum

# draw comparison of house price/income value between Melbourne and Sydney 

comparison_x = ['Melbourne','Sydney']
comparison_y = [melb_average,syd_average]

plt.figure(figsize=(12,6))
plt.bar(comparison_x,comparison_y)
plt.title('Comparison of house price/income value between Melbourne and Sydney',fontsize=18)

plt.savefig('../plots/Comparison.png',dpi=300)


# Bar charts for comparing house price/income for suburbs in Melbourne and Sydney

# Plot for melbourne
melb_income_house['the rate of housing price and income'] = melb_income_house[' sold_both_auction_private_treaty_averageprice']/melb_income_house[' mean_aud_2014_15']
# Sort the 10 smallest rates
melb_income_house.sort_values(by='the rate of housing price and income',axis=0,ascending=True,inplace=True)
melb_top10 = melb_income_house[0:10]
melb_top10 = melb_top10[['sa2_name16','the rate of housing price and income']]

melb_x = melb_top10['sa2_name16']
melb_y = melb_top10['the rate of housing price and income']

plt.figure(figsize=(18,4))
plt.bar(melb_x,melb_y)
plt.title('10 suburbs in Melbourne with the smallest rate of house price and income',fontsize=18)
melb_label = [re.sub("(.{16})", "\\1\n", label, 0, re.DOTALL) for label in melb_x]
plt.xticks(range(10), melb_label)
plt.savefig('../plots/Melbourne.png',dpi=300)


# Plot for Sydney
syd_income_house['the rate of housing price and income'] = syd_income_house[' sold_both_auction_private_treaty_averageprice']/syd_income_house[' mean_aud_2014_15']
# Sort the 10 smallest rates
syd_income_house.sort_values(by='the rate of housing price and income',axis=0,ascending=True,inplace=True)
syd_top10 = syd_income_house[0:10]
syd_top10 = syd_top10[['sa2_name16','the rate of housing price and income']]

syd_x = syd_top10['sa2_name16']
syd_y = syd_top10['the rate of housing price and income']

plt.figure(figsize=(18,4))
plt.bar(syd_x,syd_y)
plt.title('10 suburbs in Sydney with the smallest rate of house price and income',fontsize=18)
syd_label = [re.sub("(.{16})", "\\1\n", label, 0, re.DOTALL) for label in syd_x]
plt.xticks(range(10), syd_label)
plt.savefig('../plots/Sydney.png',dpi=300)



