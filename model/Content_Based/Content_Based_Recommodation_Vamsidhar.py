#!/usr/bin/env python
# coding: utf-8

# # Content Based Recommodation

# Similar content is recommended using attributes of the content.Because it uses attributes or tags of the content, such as book title, author, and rating, new books can be recommended immediately.

# ### Content-based filtering

# Using user ratings of books he/she read, we can look through the metadata of the favourite books (e.g. title, genre, author, description, keywords) and find similar titles. Basically, if a user enjoys one book, then he or she will enjoy a similar book as well.

# Pros:Quick, easy to understand (= transparent to users), no need for other users' ratings (will work even with low numbers of users), and more reliable in the beginning of the algorithm
# 
# Cons: By relying on metadata, with more features, we risk recommending the same genres and topics, there will be no diversity and novelty, so recommendations won't be personalized

# ## Importing Libraries

# In[2]:


import pandas as pd
import numpy as np


# In[3]:


import re
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# ## Importing Datasets

# In[4]:


vamsidhar_books_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/books_data.csv')
vamsidhar_ratings_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/books_ratings_data.csv')
vamsidhar_book_tags_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/book_tags_data.csv')
vamsidhar_tags_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/tags_data.csv')


# ### Checking the data 

# In[46]:


vamsidhar_books_data


# #### This method uses attributes of the content to recommend similar content. It doesn’t have a cold-start problem because it works through attributes or tags of the content, such as book title, authors or rating, so that new book can be recommended right away.

# In[8]:


content_data = vamsidhar_books_data[['original_title','authors','average_rating']]
content_data = content_data.astype(str)


# In[9]:


content_data['content'] = content_data['original_title'] + ' ' + content_data['authors'] + ' ' + content_data['average_rating']


# In[10]:


content_data = content_data.reset_index()
indices = pd.Series(content_data.index, index=content_data['original_title'])


# # Content Based Recommodation Author

# ### Removing stopwords

# In[11]:


tfidf = TfidfVectorizer(stop_words='english')


# ### Construct the required TF-IDF matrix by fitting and transforming the data
# 

# In[13]:


tfidf_matrix = tfidf.fit_transform(content_data['authors'])


# ### Output the shape of tfidf_matrix

# In[14]:


tfidf_matrix.shape


# ###### By using TF-IDF encoding, a term (a tag for a book in our example) will be weighed according to the importance of the term within the document: The more frequently the term appears, the larger its weight.Likewise, it weighs the item inversely to its frequency across the overall dataset: It will emphasize terms that are relatively rare occurrences in the general dataset but important to the specific content at hand.Words such as 'is', 'are', 'by' or 'a' that are likely to appear in every book's content, but are not useful for user recommendations, will be weighed less heavily than words that are specific to the content we are recommending.

# # Compute the cosine similarity matrix

# We are going to use a simple similarity-based method called cosine similarity

# In[51]:


cosine_sim_author = linear_kernel(tfidf_matrix, tfidf_matrix)


# # Author Wise Recommodation

# In[52]:


def get_books_recommendations(title, cosine_sim=cosine_sim_author):
    idx = indices[title]

    # Get the pairwsie similarity scores of all books with that book
    sim_score = list(enumerate(cosine_sim_author[idx]))

    # Sort the books based on the similarity scores
    sim_score = sorted(sim_score, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar books
    sim_score = sim_score[1:11]

    # Get the book indices
    book_indices = [i[0] for i in sim_score]

    # Return the top 10 most similar books
    return list(content_data['original_title'].iloc[book_indices])


# In[53]:


def author_bookshows(book):
    for book in book:
        print(book)


# ### Recommending book using title 'The Hobbit'  

# In[54]:


vamsi_books1 = get_books_recommendations('The Hobbit', cosine_sim_author)
author_bookshows(vamsi_books1)


# ### Recommending book using title 'Shadow kiss'  

# In[55]:


vamsi_books2 =get_books_recommendations('Shadow Kiss', cosine_sim_author)
author_bookshows(vamsi_books2)


# ### Recommending book using title 'Harry Potter and the Goblet of Fire'

# In[56]:


vamsi_books3 = get_books_recommendations('Harry Potter and the Goblet of Fire', cosine_sim_author)
author_bookshows(vamsi_books3)


# # Content Based Filtering On Multiple Matrix

# #### creating count and count matrix variables and generating cosine_sim_content using count and count martix

# In[70]:


count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(content_data['content'])

cosine_sim_content = cosine_similarity(count_matrix, count_matrix)


# In[71]:


def get_book_recom(title, cosine_sim=cosine_sim_content):
    idx = indices[title]

    # Get the pairwsie similarity scores of all books with that book
    sim_scores = list(enumerate(cosine_sim_content[idx]))

    # Sort the books based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar books
    sim_scores = sim_scores[1:11]

    # Get the book indices
    book_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar books
    return list(content_data['original_title'].iloc[book_indices])


# In[72]:


def bookshow(book):
    for book in book:
        print(book)


# In[ ]:


### Recommending book using title 'The Hobbit'


# In[73]:


vamsi_books4 = get_recommendations('The Hobbit', cosine_sim_content)
bookshow(vamsi_books4)


# In[ ]:


### Recommending book using title 'Shadow Kiss'


# In[74]:


vamsi_books5 =get_recommendations('Shadow Kiss', cosine_sim_content)
bookshow(vamsi_books5)


# In[ ]:


### Recommending book using title 'Harry Potter and the Goblet of Fire'


# In[75]:


vamsi_books6 =get_recommendations('The Two Towers', cosine_sim_content)
bookshow(vamsi_books6)


# In[ ]:


### Recommending book using title 'Harry Potter and the Goblet of Fire'


# In[76]:


vamsi_books7 = get_recommendations('Harry Potter and the Goblet of Fire', cosine_sim_content)
bookshow(vamsi_books7)


# In[130]:


global metric,k
k=10
metric='cosine'


# In[ ]:





# In[135]:


get_ipython().system('jupyter nbconvert Data*.ipynb --to python')


# In[ ]:




