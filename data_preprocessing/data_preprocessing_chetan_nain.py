#!/usr/bin/env python
# coding: utf-8

# # Data Preprocessing
# 
# 

# ### Importing the required libraries

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from pyecharts.charts import Bar
from pyecharts import options as opts
import warnings
warnings.filterwarnings('ignore')
import missingno as msno
from pandas import Series, DataFrame
import nltk
import json
import re
import csv
from tqdm import tqdm
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Loading the data

# In[273]:


books_data = pd.read_csv('../data/books_data.csv')
ratings_data = pd.read_csv('../data/books_ratings_data.csv')
book_tags_data = pd.read_csv('../data/book_tags_data.csv')
tags_data = pd.read_csv('../data/tags_data.csv')


# ### Understanding the loaded data and checking shape

# In[274]:


books_data.head()


# In[275]:


books_data.shape


# ### Understanding the null values in the dataset

# In[276]:


books_data.isnull().sum()


# In[277]:


msno.matrix(books_data)


# ### Removing unnecessary columns

# Since isbn13 is more precise form of coding than isbn which is just a 10 digit number so with the presence of isbn13 we wont be needing isbn. So dropping isbn from the dataset.
# 
# Similarly, best_book_id is the book id of the latest version of the book available, so we feel that we wont be needing the book_id since we already have best_book_id.
# 
# Apart form that original title too is a redundant column because of the presence of title column.

# In[278]:


books_data = books_data.drop(['book_id', 'isbn','original_title'], axis=1)


# ### Handling nulls in the dataset by imputing the values of language code (text data)

# ### Now as we know, the column 'language_code' has a lot of null values. So we will try to impute these null values.

# In[279]:


nan_in_col  = books_data[books_data['language_code'].isna()]


# In[239]:


nan_in_col


# ### As from the above analysis we can see that 1084 rows have null values. This number of data is huge and cannot be ignored.
# 
# ### To solve this problem, lets take a small subset of data from the large dataset. 
# ### In the below example I am taking the subset of data whose author is 'Charles Dickens'

# In[282]:


charlesDickens = books_data[books_data['authors']=='Charles Dickens']
charlesDickens


# ### Applying the lambda function to replace the null values with the languages of the author who have written any other book in the dataset. We can pick the language code from any other book written by the author and can replace the null values. 
# 
# ### Just like we have done for Charles Dickens, The book with title 'The Christmas Carol' was missing the language code in the above dataset, but from the dataset we know Charles Dickens has written multiple books in English. So we will impute the values and replace the null values with the language code of the mode value obtained. 
# 
# ### This way  we were able to retrieve around 50% of the missing values from the dataset.

# In[283]:


books_data['language_code'].fillna('unknown',inplace=True)
books_data['language_code'] = books_data.groupby('authors')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# ### Now checking the data of Charles Dickens again we can see that the author of A Christmas Carol is imputed correctly

# In[284]:


charlesDickens = books_data[books_data['authors']=='Charles Dickens']
charlesDickens


# ### Now checking the values that are still marked us 'unknown'

# In[285]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Since we have 584 values still marked as unknown, we will try and impute using the title of the book just in case there are some multiple entries of the same book

# In[286]:


books_data['language_code'] = books_data.groupby('title')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# ### Now checking the shape of the dataset again

# In[287]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Now imputing the same with the image url and checking the shape again

# In[288]:


books_data['language_code'] = books_data.groupby('image_url')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# In[289]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Now finally we were able to bring down the null values count to 267 from a count of 1000+

# In[255]:


msno.matrix(books_data)


# In[9]:


ratings_data.head()


# In[10]:


ratings_data.shape


# In[17]:


ratings_data.isnull().sum()


# In[11]:


book_tags_data.head()


# In[12]:


book_tags_data.shape


# In[19]:


book_tags_data.isnull().sum()


# In[13]:


tags_data.head()


# In[14]:


tags_data.shape


# In[18]:


tags_data.isnull().sum()


# ## Authors

# ## Cleaning the data for multiple authors so that the authors that are comma separated can be  splitted into multiple rows. This way they can come under proper analysis.

# ### Lets start with counting the total number of books by every author

# In[83]:


books_data['authors'].value_counts()


# ### Now from the above analysis we can see that the author Dean Koontz have written 47 books. But this may not be correct as the script is picking up only those books which have only Dean Koontz as author and not the books where Dean Koontz is a co-author

# ### The below script will help us picking up values where Dean Koontz is a co author as well.

# In[290]:


DKBooks = []
books_data['authors'].apply(lambda p: DKBooks.append(p) if 'Dean Koontz' in p else [])
DKBooks


# ### So as per the actual analysis, the total books published by Dean Koontz is 64

# In[87]:


len(DKBooks)


# ### The total number of books by multiple authors in the dataset are

# In[109]:


len(auth_books)


# ### Trying to figure out the actual number of books written by a specific author so that it can be included in analysis

# In[108]:


auth_books = []
books_data.authors.apply(lambda p: auth_books.append(p) if ',' in p else [])
auth_books[:20]


# ### Splitting the data with comma separated values and then removing the actual author column and joining with the new splitted column

# In[291]:


splittedData = books_data['authors'].str.split(',').apply(Series, 1).stack()


# In[292]:


splittedData.index = splittedData.index.droplevel(-1)


# In[293]:


splittedData.name = 'authors'


# In[294]:


del books_data['authors']


# In[295]:


books_data=books_data.join(splittedData)


# In[296]:


books_data


# ### Now as we can see that the authors data in the dataset is cleaned and now we have authors column splitted into multiple rows so that we have only one author per row.
# 
# ### And this is proved by the following scripts.

# In[269]:


auth_books = []
books_data.authors.apply(lambda p: auth_books.append(p) if ',' in p else [])
auth_books[:20]


# In[270]:


len(auth_books)


# ## Data Exploratory Analysis

# ### Understanding the outliars using box plots

# ### Drawing a box plot to understand the spread of average ratings.

# In[280]:


plt.figure(figsize=(8,4))
sns.boxplot(data=books_data['average_rating'])


# ### Drawing a box plot for understanding the spread of publication year.

# In[105]:


plt.figure(figsize=(8,4))
sns.boxplot(data=books_data['original_publication_year'])


# ### Drawing a scatter plot for understanding the distribution of ratings_5 vs average_ratings

# In[70]:


plt.figure(figsize=(28,10))
sns.lmplot(x='average_rating', y='ratings_5', data=books_data)


# ### Sorting data according to the average ratings

# In[56]:


sortedData = books_data[books_data['ratings_count']>=1500]
sortedData = sortedData.sort_values('average_rating', ascending=False)
sortedData.head()


# In[57]:


plt.figure(figsize=(15,12))
ax = sns.barplot(x=sortedData['average_rating'].head(15), y=sortedData['title'].head(15), data=sortedData)
plt.title('Best ' + str(15) + ' books by ' + 'average_rating'.replace('_',' ').capitalize(), weight='bold')
plt.xlabel('Score of ' + 'average_rating')
plt.ylabel('Book Title')


# ## Count of books written in different languages

# In[62]:


langCounts = pd.DataFrame(books_data['language_code'].value_counts())
langCounts.columns = ['Total Counts']
langCounts = langCounts.sort_values('Total Counts', ascending=False)
langCounts


# In[71]:


len(langCounts)


# In[78]:


plt.figure(figsize=(16,8))
plt.title("Books Released Language Wise")
plt.bar(x=langCounts.index,height='Total Counts', data=langCounts);


# In[74]:


langCounts = langCounts.drop(["en-US", "en-GB", "eng", "en-CA"])


# In[79]:


plt.figure(figsize=(16,8))
plt.title("Books Released Language Wise (Excluding English)")
plt.bar(x=langCounts.index,height='Total Counts', data=langCounts);


# In[299]:


get_ipython().system('jupyter nbconvert data_pre*.ipynb --to python')


# ## Adding Summary Dataset

# In[ ]:




