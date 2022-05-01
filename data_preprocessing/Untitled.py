#!/usr/bin/env python
# coding: utf-8

# # Book Recommendation System
# 
# ## Team 12
# 
# ## Chetan Nain (015761122)

# ### Python statements that imports libraries and data

# In[81]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


# In[82]:


books_data = pd.read_csv("../data/Books.csv")
users_data = pd.read_csv("../data/Users.csv")
ratings_data = pd.read_csv("../data/Ratings.csv")


# In[83]:


books_data.head()


# In[84]:


users_data.head()


# In[85]:


ratings_data.head()


# In[86]:


books_data.isnull().sum()


# In[87]:


users_data.isnull().sum()


# In[88]:


ratings_data.isnull().sum()


# ### Renaming columns and cleaning data in the dataframes

# In[ ]:





# In[97]:


users_data['City'] = users_data['Location'].str.split(',', expand=True)[0]
users_data['State'] = users_data['Location'].str.split(',', expand=True)[1]
users_data['Country'] = users_data['Location'].str.split(',', expand=True)[2]

users_data['City'] = users_data['City'].str.strip()
users_data['State'] = users_data['State'].str.strip()
users_data['Country'] = users_data['Country'].str.strip()


# In[98]:


users_data.drop(columns=['Location'])


# In[99]:


merged_df = pd.merge(ratings_data,users_data, how="inner")


# In[100]:


merged_df.head()


# In[101]:


df = pd.merge(merged_df, books_data, how = "inner")


# In[102]:


df.head()


# ## Data Exploration Step

# In[103]:


df.isnull().sum()


# In[104]:


df.describe()


# In[105]:


df.info()


# ### Bar chart to show top books from Cincinnati in the Year 1996

# In[135]:


top_ten = top_ten = df[(df['Year-Of-Publication']==1996) & (df['Book-Rating']== 10) & (df['City']=='cincinnati')]

top_ten = top_ten.sort_values(by='Book-Title', ascending=True).head(15)

plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(15,15))

sns.barplot(x='Book-Rating', y='Book-Title', data=top_ten, palette='inferno')


# In[137]:


# Books with ratings = 0
df = df[df['Book-Rating']== 0]
df.shape


# ### Authors with maximum numbers of books

# In[138]:


book_aut = df.groupby('Book-Author')['Book-Title'].count().reset_index().sort_values('Book-Title', ascending=False).head(10).set_index('Book-Author')


# In[139]:


book_aut


# In[ ]:





# In[141]:


get_ipython().system('jupyter nbconvert *.ipynb --to python')


# In[ ]:




