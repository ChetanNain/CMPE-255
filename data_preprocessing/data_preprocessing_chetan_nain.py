#!/usr/bin/env python
# coding: utf-8

# # Data Preprocessing
# 
# 

# ### Importing the required libraries

# In[154]:


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
import sys
import urllib.request
import urllib.parse
import json
import time
import re
import requests
import urllib3
from urllib.error import HTTPError
pd.set_option('display.max_rows',None)
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Loading the data

# In[364]:


books_data = pd.read_csv('../data/books_data.csv')
ratings_data = pd.read_csv('../data/books_ratings_data.csv')
book_tags_data = pd.read_csv('../data/book_tags_data.csv')
tags_data = pd.read_csv('../data/tags_data.csv')


# ### Understanding the loaded data and checking shape

# In[230]:


books_data.head()


# In[231]:


books_data.shape


# ### Understanding the null values in the dataset

# In[232]:


books_data.isnull().sum()


# In[233]:


books_data['original_title'][books_data['isbn13']==9780451524940]


# In[234]:


books_data[books_data['isbn13']==9780451524940]


# In[235]:


msno.matrix(books_data)


# ### Removing unnecessary columns

# Since isbn13 is more precise form of coding than isbn which is just a 10 digit number so with the presence of isbn13 we wont be needing isbn. So dropping isbn from the dataset.
# 
# Apart form that original title too is a redundant column because of the presence of title column.

# In[236]:


books_data = books_data.drop([ 'isbn','original_title'], axis=1)


# ### Handling nulls in the dataset by imputing the values of language code (text data)

# ### Now as we know, the column 'language_code' has a lot of null values. So we will try to impute these null values.

# In[237]:


nan_in_col  = books_data[books_data['language_code'].isna()]


# In[238]:


nan_in_col


# ### As from the above analysis we can see that 1084 rows have null values. This number of data is huge and cannot be ignored.
# 
# ### To solve this problem, lets take a small subset of data from the large dataset. 
# ### In the below example I am taking the subset of data whose author is 'Charles Dickens'

# In[239]:


charlesDickens = books_data[books_data['authors']=='Charles Dickens']
charlesDickens


# ### Applying the lambda function to replace the null values with the languages of the author who have written any other book in the dataset. We can pick the language code from any other book written by the author and can replace the null values. 
# 
# ### Just like we have done for Charles Dickens, The book with title 'The Christmas Carol' was missing the language code in the above dataset, but from the dataset we know Charles Dickens has written multiple books in English. So we will impute the values and replace the null values with the language code of the mode value obtained. 
# 
# ### This way  we were able to retrieve around 50% of the missing values from the dataset.

# In[240]:


books_data['language_code'].fillna('unknown',inplace=True)
books_data['language_code'] = books_data.groupby('authors')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# ### Now checking the data of Charles Dickens again we can see that the author of A Christmas Carol is imputed correctly

# In[241]:


charlesDickens = books_data[books_data['authors']=='Charles Dickens']
charlesDickens


# ### Now checking the values that are still marked us 'unknown'

# In[242]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Since we have 584 values still marked as unknown, we will try and impute using the authors of the book just in case there are authors of similar books.

# In[243]:


books_data['language_code'] = books_data.groupby('title')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# In[244]:


books_data['language_code'] = books_data.groupby('authors')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# In[245]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# In[246]:


# books_data['language_code'] = books_data.groupby('isbn13')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# ### Now checking the shape of the dataset again

# In[247]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Now imputing the same with the image url and checking the shape again

# In[248]:


books_data['language_code'] = books_data.groupby('image_url')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# In[249]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Now finally we were able to bring down the null values count to 267 from a count of 1000+

# Dropping these unknown rows from the dataset and the rows which has isbn13 as null.

# In[250]:


books_data.drop(books_data[books_data['language_code'] == 'unknown'].index, inplace = True)


# In[251]:


books_data= books_data.dropna()
books_data['isbn13'] = books_data['isbn13'].astype(int)


# In[252]:


msno.matrix(books_data)


# In[253]:


ratings_data.head()


# In[254]:


ratings_data.shape


# In[255]:


ratings_data.isnull().sum()


# In[256]:


book_tags_data.head()


# In[257]:


book_tags_data.shape


# In[258]:


book_tags_data.isnull().sum()


# In[259]:


tags_data


# In[261]:


tags_data.shape


# In[262]:


tags_data.isnull().sum()


# ## Authors

# ## Cleaning the data for multiple authors so that the authors that are comma separated can be  splitted into multiple rows. This way they can come under proper analysis.

# ### Lets start with counting the total number of books by every author

# In[263]:


books_data['authors'].value_counts()


# ### Now from the above analysis we can see that the author Dean Koontz have written 47 books. But this may not be correct as the script is picking up only those books which have only Dean Koontz as author and not the books where Dean Koontz is a co-author

# ### The below script will help us picking up values where Dean Koontz is a co author as well.

# In[264]:


DKBooks = []
books_data['authors'].apply(lambda p: DKBooks.append(p) if 'Dean Koontz' in p else [])
DKBooks


# ### So as per the actual analysis, the total books published by Dean Koontz is 64

# In[265]:


len(DKBooks)


# ### The total number of books by multiple authors in the dataset are

# ### Trying to figure out the actual number of books written by a specific author so that it can be included in analysis

# In[266]:


auth_books = []
books_data.authors.apply(lambda p: auth_books.append(p) if ',' in p else [])
auth_books[:20]


# In[267]:


len(auth_books)


# ### Splitting the data with comma separated values and then removing the actual author column and joining with the new splitted column

# In[268]:


splittedData = books_data['authors'].str.split(',').apply(Series, 1).stack()


# In[269]:


splittedData.index = splittedData.index.droplevel(-1)


# In[270]:


splittedData.name = 'authors'


# In[271]:


del books_data['authors']


# In[272]:


books_data=books_data.join(splittedData)


# In[273]:


books_data[books_data['best_book_id']==843]


# In[274]:


books_data.head()


# ### Now as we can see that the authors data in the dataset is cleaned and now we have authors column splitted into multiple rows so that we have only one author per row.
# 
# ### And this is proved by the following scripts.

# In[275]:


auth_books = []
books_data.authors.apply(lambda p: auth_books.append(p) if ',' in p else [])
auth_books[:20]


# In[276]:


len(auth_books)


# ## Data Exploratory Analysis

# ### Understanding the outliars using box plots

# ### Drawing a box plot to understand the spread of average ratings.

# In[210]:


plt.figure(figsize=(8,4))
sns.boxplot(data=books_data['average_rating'])


# ### Drawing a box plot for understanding the spread of publication year.

# In[211]:


plt.figure(figsize=(8,4))
sns.boxplot(data=books_data['original_publication_year'])


# ### Drawing a scatter plot for understanding the distribution of ratings_5 vs average_ratings

# In[212]:


plt.figure(figsize=(28,10))
sns.lmplot(x='average_rating', y='ratings_5', data=books_data)


# ### Sorting data according to the average ratings

# In[213]:


sortedData = books_data[books_data['ratings_count']>=1500]
sortedData = sortedData.sort_values('average_rating', ascending=False)
sortedData.head()


# In[214]:


plt.figure(figsize=(15,12))
ax = sns.barplot(x=sortedData['average_rating'].head(15), y=sortedData['title'].head(15), data=sortedData)
plt.title('Best ' + str(15) + ' books by ' + 'average_rating'.replace('_',' ').capitalize(), weight='bold')
plt.xlabel('Score of ' + 'average_rating')
plt.ylabel('Book Title')


# ## Count of books written in different languages

# In[215]:


langCounts = pd.DataFrame(books_data['language_code'].value_counts())
langCounts.columns = ['Total Counts']
langCounts = langCounts.sort_values('Total Counts', ascending=False)
langCounts


# In[216]:


len(langCounts)


# In[217]:


plt.figure(figsize=(16,8))
plt.title("Books Released Language Wise")
plt.bar(x=langCounts.index,height='Total Counts', data=langCounts);


# In[218]:


langCounts = langCounts.drop(["en-US", "en-GB", "eng", "en-CA"])


# In[219]:


plt.figure(figsize=(16,8))
plt.title("Books Released Language Wise (Excluding English)")
plt.bar(x=langCounts.index,height='Total Counts', data=langCounts);


# ## Adding Summary Dataset

# In[277]:


books_data.shape


# In[278]:


books_data.head(2)


# In[287]:


books_data['summary']=''
books_data['genre']=''
#HTTPError as err


# In[351]:


while True:
    try:
        for index, row in books_data.iterrows():
            if pd.isna(row['summary']):
                print(row['title'])
                time.sleep(0.5)
                req = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(row['isbn13'])
                res = urllib.request.urlopen(req)
                result = json.loads(res.read().decode('utf-8'))
                if 'items' in result:
                    if 'volumeInfo' in result['items'][0]:
                        if 'description' in result['items'][0]['volumeInfo']:
                            print(row['title'])
                            books_data.at[index , 'summary'] = result['items'][0]['volumeInfo']['description']
                        if 'categories' in result['items'][0]['volumeInfo']:
                            books_data.at[index , 'genre'] = result['items'][0]['volumeInfo']['categories'][0]
                        else:
                            books_data.at[index , 'summary']=np.nan
                    else:
                        books_data.at[index , 'summary']=np.nan
        #                 row['summary']=result['items'][0]['volumeInfo']['description']
                else:
                    books_data.at[index , 'summary']=np.nan
    except HTTPError as err:
        print(err)


# In[322]:


for col in books_data.columns:
    print(col)


# In[327]:


books_data[books_data['summary']==''].shape


# In[326]:


books_data[books_data['summary']==np.nan].shape


# In[356]:


books_data.head(10)


# In[374]:


books_data = books_data.dropna()


# In[375]:


books_data = books_data[books_data['summary']!='']


# In[376]:


books_data.head(20)


# In[377]:


books_data.to_csv("cleaned_books_data.csv")


# In[ ]:


get_ipython().system('jupyter nbconvert data_pre*.ipynb --to python')


# In[76]:


# Extra function that can be used to clean summaries incase they are not clean.
def clean_summary(text):
    text = re.sub("\'", "", text)
    text = re.sub("[^a-zA-Z]"," ",text)
    text = ' '.join(text.split())
    text = text.lower()
    return text

