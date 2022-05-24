#!/usr/bin/env python
# coding: utf-8

# ## Content Based Model Using Sigmoid Kernel

# ### Content-based recommendation algorithms are more concerned with item characteristics or qualities than with user data. They forecast a user's behavior based on the objects to which they respond. 
# 
# ### Finding a decent movie to binge-watch over the weekend without having to do too much research is a typical challenge that millennials face nowadays. Let's look at how we might fix this problem for millennials by assisting them in finding a movie that they are likely to appreciate.

# In[1]:


import pandas as pd
import numpy as np


# ### Importing Data from the dataset

# In[2]:


books_data = pd.read_csv('../../data_preprocessing/cleaned_books_data.csv')
books_data=books_data.dropna()


# ### Lets understand the data by taking a sample of it. Lets look at the books written by George Orwell.

# In[3]:


books_data[books_data['authors']=='George Orwell']


# ### Before we begin the analysis, lets check for null data in the dataset.

# In[4]:


books_data.isnull().sum()


# ### We'll need to transform our text in the summary column to word vectors and fit a TF-IDF on overview before we can conduct any analysis on the plot summaries:

# In[5]:


from sklearn.feature_extraction.text import TfidfVectorizer


# In[6]:


tvf = TfidfVectorizer(min_df=3, max_features=None, strip_accents='unicode', analyzer='word', ngram_range=(1,3), token_pattern=r'\w{1,}', stop_words='english')


# In[ ]:





# In[7]:


tvf_matrix = tvf.fit_transform(books_data['summary'])


# In[8]:


tvf_matrix.shape


# ### So, to describe our 10,000 books, summaries employed roughly 63,500 unique words. This figure can be changed depending on the ngram range passed to the function parameter.

# ### Now that we have a word matrix, we can start computing similarity scores. This measure will assist us in identifying summary with plot descriptions comparable to the one provided by the user.

# ### With the below code we will start computing the sigmoid kernel

# In[9]:


from sklearn.metrics.pairwise import sigmoid_kernel
sig = sigmoid_kernel(tvf_matrix, tvf_matrix)


# In[10]:


sig[0]


# ### Now to proceed ahead we will do reverse mapping of indices and books title.

# In[11]:


indices= pd.Series(books_data.index, index=books_data['title']).drop_duplicates()


# In[12]:


indices


# In[13]:


def give_recom(title, sig=sig):
    # we will start by pulling the index of a given titile
    idx=indices[title]
    #We will get the pairwise similarity score.
    sig_score = list(enumerate(sig[idx]))
    # we will sort the movies.
    sig_score = sorted(sig_score, key=lambda x:x[1], reverse=True)
    # return the sigma score of top 10 similar books 
    sig_score = sig_score[1:101]
    book_indices = [i[0] for i in sig_score]
    #writing the data to an external file 
    output_file = open('content_op.txt', 'w')
    output_file.write("\n".join([str(x) for x in book_indices]))
    output_file.close()
    # Finally returning the data.
    return books_data['title'].iloc[book_indices]


# In[14]:


# Finally returning top unique books.
give_recom('The Great Gatsby').head(10).unique()


# In[15]:


get_ipython().system('jupyter nbconvert Content_Based_Chetan_Nain*.ipynb --to python')


# In[ ]:




