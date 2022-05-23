#!/usr/bin/env python
# coding: utf-8

# ## Collaborative Filtering Using k-Nearest Neighbors (kNN)

# Collaborative filtering based on k-nearest neighbors (kNN) kNN is a machine learning algorithm thats finds clusters of similar users based on thier book ratings, and making predictions based on the average of the top (kNN) k-nearest neighbors

# K-nearest neighbors (KNN) is a simple, supervised machine learning algorithm that can be used for both classification and regression. This method is easy to implement and understand, but it becomes significantly slow as the size of the data in use increases.
# 
# k is a positive integer
# 
# N (Nearest)
# 
# N (Neighbors)

# ## Importing Libraries

# In[47]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


# ## Importing Datasets

# In[48]:


vamsidhar_books = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/books_data.csv')
vamsidhar_ratings  = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/books_ratings_data.csv')
vamsidhar_book_tags = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/book_tags_data.csv')
vamsidhar_tags = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/tags_data.csv')


# In[68]:


vamsidhar_books


# In[49]:


#pd.set_option('display.max_columns', 10)


# In[50]:


vamsidhar_books.head()


# In[51]:


vamsidhar_books.describe()


# ## vamsidhar_ratings info

# In[52]:


vamsidhar_ratings.head()


# In[53]:


vamsidhar_ratings.describe()


# ### Removing outliers

# In[54]:


vamsidhar_books = vamsidhar_books.dropna()
vamsidhar_ratings = vamsidhar_ratings.sort_values("user_id")
vamsidhar_ratings.drop_duplicates(subset=["user_id","book_id"], keep='first', inplace=True) 
vamsidhar_books.drop_duplicates(subset='original_title', keep='first', inplace=True)


# ###  Using KNN

# In[55]:


vamsidhar_merged_df = pd.merge(vamsidhar_books, vamsidhar_ratings, how='left', left_on=['id'], right_on=['book_id'])
vamsidhar_df = vamsidhar_merged_df[['id','original_title', 'user_id', 'rating']]

vamsidhar_df = vamsidhar_df.rename(columns = {'id':'book_id'})
vamsidhar_df.head(200)


# In[56]:


vamsidhar_df.describe()


# In[57]:


vamsidhar_ratings = vamsidhar_df.pivot_table(index='book_id',columns='user_id',values='rating').fillna(0)

#pd.set_option('display.max_columns', 100)
vamsidhar_ratings.head()


# In[58]:


vamsidhar_ratings.shape


# In[59]:


vamsidhar_ratings_matrix = csr_matrix(vamsidhar_ratings.values)


# ### Training model

# In[60]:


vamsidhar_model_knn = NearestNeighbors(metric='cosine', algorithm = 'brute')
vamsidhar_model_knn.fit(vamsidhar_ratings_matrix)


# ### Some Helper Functions

# #### Function which returns book title locations 

# In[61]:


def get_book_id(book_title):
    vamsi_target_df = vamsidhar_df.loc[vamsidhar_df['original_title'] == book_title]
    return vamsi_target_df['book_id'].iloc[0]

id_BayouMoon = get_book_id('Bayou Moon')
print(id_BayouMoon)


# #### Function which returns book id locations 

# In[62]:


def get_title(book_id):
    vamsi_target_df = vamsidhar_df.loc[vamsidhar_df['book_id'] == book_id]
    return vamsi_target_df['original_title'].iloc[0]

print(get_title(1))


# ### This function returns book recommendations using book title

# In[63]:


def get_recomm(book_title, num_neighbors=10, display=False): 
    vamsi_book_ids = []
    
    query_index = get_book_id(book_title) - 1
    
    if num_neighbors > 0:
        distances, indices = vamsidhar_model_knn.kneighbors(vamsidhar_ratings.iloc[query_index,:].values.reshape(1, -1), n_neighbors = num_neighbors + 1)
    else:
        distances, indices = vamsidhar_model_knn.kneighbors(vamsidhar_ratings.iloc[query_index,:].values.reshape(1, -1), n_neighbors = 10 + 1)
    
    for i in range(0, len(distances.flatten())):
        if display is True:
            if i == 0:
                print('Recommendations for ', book_title, '\n')
            else:    
                print('{0}\t Book ID: {1}\t  Distance: {2}:\n'.format(i, vamsidhar_ratings.index[indices.flatten()[i]], distances.flatten()[i]))
        
        vamsi_book_ids.append(vamsidhar_ratings.index[indices.flatten()[i]])
    
    return vamsi_book_ids


# ### Test the Results

# ### Top 15 recommendations for Harry Potter and the Philosopher's Stone

# In[64]:


recommendations_for_HarryPotterandthePhilosophersStone = get_recomm("Harry Potter and the Philosopher's Stone", num_neighbors=15, display=True)


# In[65]:


for b in recommendations_for_HarryPotterandthePhilosophersStone[1:]:
    print('id:', b, '\t\tBook: ', get_title(b))


# ### Top 15 recommendations for To Kill a Mockingbird

# In[66]:


book_ids_for_H = get_recomm('To Kill a Mockingbird', num_neighbors=15)
for b in book_ids_for_H[1:]:
    print(get_title(b))


# ### Top 20 recommendations for The Great Gatsby

# In[67]:


book_ids_for_H = get_recomm('The Great Gatsby', num_neighbors=20)
for b in book_ids_for_H[1:]:
    print(get_title(b))


# In[ ]:


Converting


# In[ ]:




