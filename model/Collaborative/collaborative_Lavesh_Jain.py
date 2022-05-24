#!/usr/bin/env python
# coding: utf-8

# #### Collaborative Filtering

# In[1]:


import warnings
warnings.filterwarnings('ignore')


# In[2]:


import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')


# In[3]:


# books_data = pd.read_csv('../data/books_data.csv')
books_data = pd.read_csv('../../data_preprocessing/cleaned_books_data.csv')
ratings_data = pd.read_csv('../../data/books_ratings_data.csv')
book_tags_data = pd.read_csv('../../data/book_tags_data.csv')
tags_data = pd.read_csv('../../data/tags_data.csv')


# In[4]:


# Added to remove unnamed column from preprocessed dataset

books_data.dropna(inplace=True)


# In[5]:


# Cleaning 'original_publication_year' -> move to preprocessing later
books_data['original_publication_year'] = books_data['original_publication_year'].fillna(-1).apply(lambda x: int(x) if x != -1 else -1)


# In[6]:


# Removing duplicate ratings
unique_ratings = ratings_data.drop_duplicates()

# removing users with less than 4 ratings
unwanted_users = unique_ratings.groupby('user_id')['user_id'].count()
unwanted_users = unwanted_users[unwanted_users < 4]
unwanted_ratings = unique_ratings[unique_ratings.user_id.isin(unwanted_users.index)]
filtered_ratings = unique_ratings.drop(unwanted_ratings.index)


# In[7]:


books_data.head(2)


# In[8]:


filtered_ratings.head()


# In[9]:


filtered_ratings = pd.merge(filtered_ratings, books_data[['id','title']], how='inner', left_on='book_id', right_on='id')


# In[10]:


filtered_ratings.head()


# ##### User based approach

# In[11]:


from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate


# In[12]:


# laod dataset to surprise from pandas dataframe - filtered_ratings
reader = Reader()
data = Dataset.load_from_df(filtered_ratings[['user_id', 'book_id', 'rating']], reader)


# In[ ]:


# perform a 5 fold cross validation
algo = SVD()
cross_validate(algo, data, measures=['RMSE', 'MAE'], cv =5)


# In[ ]:


# Build and fit model on trainset
trainset = data.build_full_trainset()
algo.fit(trainset);


# In[ ]:


# check data with user_id = 40
filtered_ratings[filtered_ratings['user_id'] == 40]


# In[ ]:


# predict how the user would rate a particular book
user_id = 50
book_id = 1000
algo.predict(user_id, book_id)


# In[ ]:


def predict_rating(user_id,book_id):
    return algo.predict(user_id, book_id)


# ##### Iten based approach

# In[ ]:


filtered_ratings[filtered_ratings['title'].str.contains('^Twi.*')==True]


# In[ ]:


bookmat = filtered_ratings.pivot_table(index='user_id', columns='title', values='rating')
bookmat.head()


# In[ ]:


def get_similar(title, mat):
    title_user_ratings = mat[title]
    similar_to_title = mat.corrwith(title_user_ratings)
    corr_title = pd.DataFrame(similar_to_title, columns=['correlation'])
    corr_title.dropna(inplace=True)
    corr_title.sort_values('correlation', ascending=False, inplace=True)
    return corr_title


# In[ ]:


bookmat.head()


# In[ ]:


bookmat['Twilight (Twilight, #1)']


# In[ ]:


title = "Twilight (Twilight, #1)"
smlr = get_similar(title, bookmat)


# In[ ]:


smlr.head(10)


# In[ ]:


# filter by rating count
smlr = smlr.join(books_data.set_index('title')['ratings_count'])
smlr.head()


# In[ ]:


smlr[smlr.ratings_count > 5e5].sort_values('correlation', ascending=False).head(10)


# In[ ]:


get_ipython().system('jupyter nbconvert collaborative_Lavesh_Jain*.ipynb --to python')


# In[ ]:




