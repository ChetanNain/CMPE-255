#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


books_data = pd.read_csv('../../data_preprocessing/books_data.csv')
books_data=books_data.dropna()


# In[3]:


books_data[books_data['authors']=='George Orwell']


# In[4]:


books_data.isnull().sum()


# In[5]:


books_data[books_data['isbn13']==9780451524940]


# In[6]:


books_data.dropna()


# In[7]:


from sklearn.feature_extraction.text import TfidfVectorizer


# In[8]:


tvf = TfidfVectorizer(min_df=3, max_features=None, strip_accents='unicode', analyzer='word', ngram_range=(1,3), token_pattern=r'\w{1,}', stop_words='english')


# In[ ]:





# In[9]:


tvf_matrix = tvf.fit_transform(books_data['summary'])


# In[10]:


tvf_matrix.shape


# In[11]:


from sklearn.metrics.pairwise import sigmoid_kernel
sig = sigmoid_kernel(tvf_matrix, tvf_matrix)


# In[12]:


sig[0]


# In[13]:


indices= pd.Series(books_data.index, index=books_data['title']).drop_duplicates()


# In[14]:


indices


# In[15]:


def give_recom(title, sig=sig):
    idx=indices[title]
    sig_score = list(enumerate(sig[idx]))
    sig_score = sorted(sig_score, key=lambda x:x[1], reverse=True)
    sig_score = sig_score[1:11]
    book_indices = [i[0] for i in sig_score]
    
    output_file = open('content_op.txt', 'w')
    output_file.write("\n".join([str(x) for x in book_indices]))
    output_file.close()
    
    return books_data['title'].iloc[book_indices]


# In[16]:


# give_recom('my sunshine away')


# In[ ]:




