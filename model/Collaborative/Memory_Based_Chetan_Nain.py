#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import defaultdict
import random
import numpy
import scipy.optimize
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


# In[2]:


books_data = pd.read_csv('../../data_preprocessing/books_data.csv')
ratings_data = pd.read_csv('../../data/books_ratings_data.csv')
book_tags_data = pd.read_csv('../../data/book_tags_data.csv')
tags_data = pd.read_csv('../../data/tags_data.csv')


# In[3]:


ratings_data = ratings_data.drop_duplicates()


# In[4]:


dataset = pd.merge(ratings_data, books_data[['id','title']], how='inner', left_on='book_id', right_on='id')


# In[5]:


dataset.head(10)


# In[6]:


unique_users = dataset['user_id'].unique()
print(len(unique_users))


# In[7]:


unique_bookId= dataset['book_id'].unique()
print(len(unique_bookId))


# In[8]:


unique_id = dataset['id'].unique()
print(len(unique_id))


# In[9]:


unique_title = dataset['title'].unique()
print(len(unique_title))


# In[10]:


new_df = pd.DataFrame(unique_users)
new_df.columns=['userId']


# In[11]:


for title in unique_title:
    new_df[title]=None


# In[15]:


for j,user in enumerate(new_df['userId'].values):
    for i in range(dataset[dataset['user_id']==user].shape[0]):
        title = dataset[dataset['user_id']==user]['title'].iloc[i]
        rating = dataset[dataset['user_id']==user]['rating'].iloc[i]
        new_df[title][j] = rating


# In[16]:


new_df.head


# In[17]:


user = pd.DataFrame(new_df.iloc[2121])
user = user.drop(['userId'])
user[user.notnull().values]


# In[18]:


subset = new_df[new_df[user[user.notnull().values].index[0]].notnull()]
subset.head()


# In[19]:


subset = subset.replace([None],0)
subset = subset.set_index('userId')


# In[20]:


subset.head()


# In[21]:


subset['similarity'] = 0.0
for user in subset.index:
    cos = cosine_similarity(subset.loc[28158].values.reshape(1,-1),subset.loc[user].values.reshape(1,-1))
    subset['similarity'][user]=cos


# In[22]:


subset['similarity']


# In[ ]:


get_ipython().system('jupyter nbconvert Data*.ipynb --to python')

