#!/usr/bin/env python
# coding: utf-8

# # Data Preprocessing

# ## Import Libraries

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import squarify
import missingno as mn
from wordcloud import WordCloud, STOPWORDS


# In[2]:


data_frame = pd.read_csv("US_Accidents_Dec20.csv")


# In[3]:


data_frame


# In[4]:


data_frame.head()


# In[5]:


data_frame.tail()


# In[6]:


data_frame.shape


# In[8]:


data_frame.index


# ### Statistical Description of each column

# In[9]:


data_frame.describe()


# ### Columns in dataframe

# In[10]:


data_frame.columns


# ### Numerical Columns to deal with

# In[11]:


print(data_frame.count(numeric_only=True))
print("Total No. of Numerical Columns:", len(data_frame.count(numeric_only=True)))


# # Check out the Missing Values

# In[12]:


import missingno as missnum
missing_val = data_frame.isna().sum().sort_values(ascending=False)
missing_percent = missing_val[missing_val!=0]/len(data_frame)*100


# In[15]:


print(" Missing Values in %\n", missing_percent)


# ### Getting List of Columns Having Null Values

# In[16]:


null_columns = [i for i in data_frame.columns if data_frame[i].isnull().any()]
print(null_columns)


# In[17]:


data_frame.isnull().sum()


# In[19]:


missnum.matrix(data_frame[null_columns]);


# # Handling Missing Data of the dataset

# In[20]:


data_frame.dropna(inplace=True)


# In[21]:


data_frame.isnull().sum()


# ### Data After Dropping missing values

# In[22]:


data_frame.shape


# In[24]:


missnum.matrix(data_frame[null_columns]);


# # Data Understanding and Exploration Analysis

# ### The feature Country has only one entry i.e USA, it is obvious since we are dealing with the USA’s dataset. so we will be deleting the feature Country.
# 
# ### The feature Turning_Loop has only one value — False. the feature actually means that no accidents were occured in the turning loops.

# In[56]:


data_frame.columns


# In[34]:


from sklearn.model_selection import train_test_split
df1 = data_frame[[column for column in data_frame if data_frame[column].count() / len(data_frame) >= 0.3]]


# ### Severity

# In[27]:


data_frame.Severity.value_counts(normalize=True).sort_index().plot.bar()
plt.grid()
plt.title('Severity')
plt.xlabel('Severity')
plt.ylabel('');


# #### Most of the US Accidents i.e 0.8 have the severity 2 and followed by severity 4.

# ### Proximity of the Traffic

# In[30]:


boolean_columns = [col for col in data_frame.columns if data_frame[col].dtype ==np.dtype('bool')]
booleandf = data_frame[boolean_columns]
meta = booleandf[booleandf.sum(axis=1) > 1]
print('There are {} metadata rows, which are {:.1f}% of the data'.format(len(meta),100*len(meta)/len(data_frame)))


# In[31]:


booleans = booleandf.sum(axis=0)


# In[32]:


booleans.plot.pie(figsize=(13,13))
plt.ylabel('')
plt.title('Proximity to Traffic');


# #### Major percentage of  the US Accidents  are occured at traffic signals, Crossing, Station, Stop and Amenity. The least percentage of  accidents are occured at Bump, Roundabout, Railway, No-Exit, Junction 

# ## Duration Of Top 20 Accidents 

# In[36]:


start = pd.to_datetime(df.Start_Time, format='%Y-%m-%d %H:%M:%S')
end = pd.to_datetime(df.End_Time, format='%Y-%m-%d %H:%M:%S')


# In[37]:


d = (end-start)
top20 = d.astype('timedelta64[m]').value_counts().nlargest(20)
print('Top 20 accident durations in US Accidents dataset data {:.1f}% '.format(top20.sum()*100/len(d)))
(top20/top20.sum()).plot.bar(figsize=(14,14))
plt.title('Overall Duration of Accident in Minutes')
plt.xlabel('Duration in Minutes')
plt.ylabel('Fraction');


# In[38]:


count_statewise = data_frame['State'].value_counts()
top10_statecount = count_statewise.iloc[:10]
other_statecount = {'Others': count_statewise.iloc[10:].values.sum()}
overall_count = top10_statecount.append(pd.Series(other_statecount))


# In[39]:


overall_count


# In[41]:


plt.figure(figsize=(15, 10))
sns.barplot(top10_statecount.index, top10_statecount.values)
plt.show()


# #### Most percentage of accidents are occured in California followed by florida.

# In[42]:


fig = go.Figure(data=go.Choropleth(
    locations=count_statewise.index,
    z = count_statewise.values,
    locationmode = 'USA-states',
    colorscale = 'Reds',
    colorbar_title = "Accidents",
))
fig.update_layout(
    title_text = 'US Accidents States wise',
    geo_scope='usa',
    width=900, height=700
)
fig.show()


# ## Accident Analysis in California
# ### As it is top most accident occured state

# In[43]:


california = data_frame[data_frame['State'] == 'CA'].groupby('County').size().sort_values(ascending=False)
california.head()


# ### Bar Graph of California accidents 

# In[44]:


plt.figure(figsize=(15, 10))
sns.barplot(california[:10].index, california[:10].values)
plt.show()


# ### Pie Chart of California accidents 

# In[46]:


plt.figure(figsize=(15, 10))
plt.pie(top10_statecount.values, labels=top10_statecount.index, autopct='%1.1f%%')
plt.show()


# ## Weather Conditions Affecting Accidents

# In[47]:


plt.figure(figsize=(15, 10))
data_frame.groupby('Weather_Condition').size().sort_values(ascending = False).iloc[:5].plot.pie(explode=[0.1,0,0,0,0],autopct='%1.1f%%',shadow=True)
plt.show()


# ## Accidents on Weekdays vs Weekends

# In[48]:


data_frame['Start_Time'] = pd.to_datetime(data_frame['Start_Time'], infer_datetime_format=True)
data_frame['End_Time'] = pd.to_datetime(data_frame['Start_Time'], infer_datetime_format=True)
data_frame['Day_of_Week'] = data_frame['Start_Time'].dt.day_name()
weekday_data = data_frame.groupby('Day_of_Week').size().sort_values(ascending = False)
weekday_data.head()


# In[49]:


plt.figure(figsize=(13, 7))
sns.barplot(weekday_data.index, weekday_data.values)
plt.show()


# ## Data Understanding from above Graphs
#     1)Most of the US Accidents i.e 0.8 have the severity 2 and followed by severity 4.
#     
#     2)Major percentage of  the US Accidents  are occured at traffic signals, Crossing, Station, Stop and Amenity. The least         percentage of  accidents are occured at Bump, Roundabout, Railway, No-Exit, Junction
#     
#     3)Most percentage of accidents are occured in California followed by florida.
#     4)Accidents are occurred in clear weather conditions(52.9%) and followed by cloudy weather 18.7% which means that weather       conditions effects very less.
#     5) Weekday Accidents are higher in number compared to weekends.

# # Data Preparation for Modeling -  training and testing sets

# In[50]:


from sklearn.model_selection import train_test_split

y = data_frame['Severity']
x = data_frame.iloc[:,2:]

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)


# In[51]:


X_train


# In[52]:


X_test


# In[53]:


y_train


# In[54]:


y_test

