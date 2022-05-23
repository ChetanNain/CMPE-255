#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[35]:


books_data = pd.read_csv('../../data_preprocessing/books_data.csv')
books_data=books_data.dropna()


# In[36]:


books_data[books_data['authors']=='George Orwell']


# In[37]:


books_data.isnull().sum()


# In[38]:


books_data[books_data['isbn13']==9780451524940]


# In[39]:


books_data.dropna()


# In[40]:


from sklearn.feature_extraction.text import TfidfVectorizer


# In[41]:


tvf = TfidfVectorizer(min_df=3, max_features=None, strip_accents='unicode', analyzer='word', ngram_range=(1,3), token_pattern=r'\w{1,}', stop_words='english')


# In[ ]:





# In[42]:


tvf_matrix = tvf.fit_transform(books_data['summary'])


# In[43]:


tvf_matrix.shape


# In[44]:


from sklearn.metrics.pairwise import sigmoid_kernel
sig = sigmoid_kernel(tvf_matrix, tvf_matrix)


# In[45]:


sig[0]


# In[46]:


indices= pd.Series(books_data.index, index=books_data['title']).drop_duplicates()


# In[47]:


indices


# In[50]:


def give_recom(title, sig=sig):
    idx=indices[title]
    sig_score = list(enumerate(sig[idx]))
    sig_score = sorted(sig_score, key=lambda x:x[1], reverse=True)
    sig_score = sig_score[1:11]
    book_indices = [i[0] for i in sig_score]
    return books_data['title'].iloc[book_indices]


# In[58]:


give_recom('my sunshine away')


# In[ ]:




