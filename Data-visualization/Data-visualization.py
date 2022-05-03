#!/usr/bin/env python
# coding: utf-8

# # Data visualization
# 
# 

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import plotly_express  as px
import warnings
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud,STOPWORDS


warnings.filterwarnings('ignore')


# In[2]:


books_data = pd.read_csv('../data/books_data.csv')
ratings_data = pd.read_csv('../data/books_ratings_data.csv')
book_tags_data = pd.read_csv('../data/book_tags_data.csv')
tags_data = pd.read_csv('../data/tags_data.csv')


# In[3]:


books_data.head()


# In[4]:


books_data.shape


# ## Data Exploratory Analysis

# ### Top Rated Books
# 
#     
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and visualize Top rated books in the dataset.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
#     -------------------
#     
#     output: bar plot to visualize Top rated books in the dataset
#     
# 

# In[5]:


def top_rated_books(books_data):
    top_rated_books = books_data.sort_values('average_rating', ascending=False)
    df_top_rated = top_rated_books[:15]
    fig = px.bar(df_top_rated, x="average_rating", y="original_title", title='Top Rated Books and Their Ratings')
    fig.update_layout(xaxis_range=[0,5])
    fig.show()
top_rated_books(books_data)


# ### Sorting data according to the average ratings

# In[6]:


sortedData = books_data[books_data['ratings_count']>=1500]
sortedData = sortedData.sort_values('average_rating', ascending=False)
sortedData.head()


# In[7]:


plt.figure(figsize=(15,12))
ax = sns.barplot(x=sortedData['average_rating'].head(15), y=sortedData['title'].head(15), data=sortedData)
plt.title('Best ' + str(15) + ' books by ' + 'average_rating'.replace('_',' ').capitalize(), weight='bold')
plt.xlabel('Score of ' + 'average_rating')
plt.ylabel('Book Title')    


# ### Average Ratings Distribution
#     
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and visualize Average ratings for the books in the dataset.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
#     -------------------
#     
#     output: Histogram to visualize Average ratings for the books in the dataset
#     
# 
# 

# In[8]:


def avg_rating(books_data):
    plt.figure(figsize=(10,5))
    books_data["average_rating"].hist()
    display()
avg_rating(books_data)


# ### Top Authors
# 
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and visualize Top Authors for the books in the dataset.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
#     -------------------
#     
#     output: Interactive Barplot to visualize top authors of books in the dataset
#     
# 
# 

# In[9]:


def topauthors(books_data):
    top_authors = books_data['authors'].value_counts().reset_index()
    top_authors.columns = ['value', 'count']
    top_authors['value'] = top_authors['value']
    top_authors = top_authors.sort_values('count')
    fig = px.bar(top_authors.tail(10), x="count", y="value", color='value',
                 width=1000, height=700)
    fig.show()
topauthors(books_data)


# ### Treemap
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and visualize dataset in form of Treemap.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
#     -------------------
#     
#     output: Treemap to visualize books in the dataset
#     
# 
# 

# In[10]:


def get_treemap(books_data):
    
    dropna= books_data.dropna()
    fig = px.treemap(dropna, path=['original_publication_year','language_code', "average_rating"],
                      color='average_rating')
    fig.show()
get_treemap(books_data)


# ### Heatmap
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and returns the correlation between all the columns.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
# 

# In[11]:


def get_heatmap(books_data):
    f,ax = plt.subplots(figsize=(10,10))
    sns.heatmap(books_data.corr(), annot=True, linewidths=0.6,linecolor="black", fmt= '.1f',ax=ax)
    plt.show() 
get_heatmap(books_data)


# ### Number of books in each year
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and returns the histogram plot to visualize the number of books published each year.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
# 
# 

# In[12]:


def get_histplot(books_data):
    sns.histplot(x="original_publication_year", data=books_data, bins=1000)
    plt.xlim(1900,2020);
get_histplot(books_data)


# ### Number of Authors Ratings Rates
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and returns the Number of Authors Ratings Rates for year 2015 and 2016.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
# 
# 
# 

# In[13]:


def getpiechart(books_data):
    df = books_data[books_data.original_publication_year == 2015].iloc[:7,:]
    pie1 = df.ratings_1
    df1 = books_data[books_data.original_publication_year == 2016].iloc[:7,:]
    pie2 = df1.ratings_1
    labels = df.authors.value_counts().index

    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=pie1, name="Number Of Authors Rates"),
                  1, 1)
    fig.add_trace(go.Pie(labels=labels, values=pie2, name="Number Of Authors Rates"),
                  1, 2)
    fig.update_traces(hole=.45, hoverinfo="label+percent+name")
    fig.update_layout(
        height=800, width=800,
        annotations=[dict(text='2015', x=0.175, y=0.5, font_size=14, showarrow=False),
                     dict(text='2016', x=0.82, y=0.5, font_size=14, showarrow=False)])
    fig.show()
getpiechart(books_data)


# ### Stopwords of Authors
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and returns the Stopwords of author.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
# 

# In[14]:


stop_words=set(STOPWORDS)
author_string = " ".join(books_data['authors'])


def getstopwords(string):
    wc = WordCloud(width=800,height=500,mask=None,random_state=21, max_font_size=110,stopwords=stop_words).generate(string)
    fig=plt.figure(figsize=(16,8))
    plt.axis('off')
    plt.imshow(wc)
getstopwords(author_string)

