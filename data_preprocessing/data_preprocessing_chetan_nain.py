#!/usr/bin/env python
# coding: utf-8

# # Data Preprocessing
# 
# 

# ### Importing the required libraries

# In[3]:


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


# In[4]:


pip install urllib3


# ### Loading the data

# In[5]:


books_data = pd.read_csv('../data/books_data.csv')
ratings_data = pd.read_csv('../data/books_ratings_data.csv')
book_tags_data = pd.read_csv('../data/book_tags_data.csv')
tags_data = pd.read_csv('../data/tags_data.csv')


# ### Understanding the loaded data and checking shape

# In[6]:


books_data.head()


# In[7]:


books_data.shape


# ### Understanding the null values in the dataset

# In[8]:


books_data.isnull().sum()


# In[12]:


books_data['original_title'][books_data['isbn13']==9780451524940]


# In[13]:


books_data[books_data['isbn13']==9780451524940]


# In[7]:


msno.matrix(books_data)


# ### Removing unnecessary columns

# Since isbn13 is more precise form of coding than isbn which is just a 10 digit number so with the presence of isbn13 we wont be needing isbn. So dropping isbn from the dataset.
# 
# Similarly, best_book_id is the book id of the latest version of the book available, so we feel that we wont be needing the book_id since we already have best_book_id.
# 
# Apart form that original title too is a redundant column because of the presence of title column.

# In[8]:


books_data = books_data.drop(['book_id', 'isbn','original_title'], axis=1)


# ### Handling nulls in the dataset by imputing the values of language code (text data)

# ### Now as we know, the column 'language_code' has a lot of null values. So we will try to impute these null values.

# In[9]:


nan_in_col  = books_data[books_data['language_code'].isna()]


# In[10]:


nan_in_col


# ### As from the above analysis we can see that 1084 rows have null values. This number of data is huge and cannot be ignored.
# 
# ### To solve this problem, lets take a small subset of data from the large dataset. 
# ### In the below example I am taking the subset of data whose author is 'Charles Dickens'

# In[11]:


charlesDickens = books_data[books_data['authors']=='Charles Dickens']
charlesDickens


# ### Applying the lambda function to replace the null values with the languages of the author who have written any other book in the dataset. We can pick the language code from any other book written by the author and can replace the null values. 
# 
# ### Just like we have done for Charles Dickens, The book with title 'The Christmas Carol' was missing the language code in the above dataset, but from the dataset we know Charles Dickens has written multiple books in English. So we will impute the values and replace the null values with the language code of the mode value obtained. 
# 
# ### This way  we were able to retrieve around 50% of the missing values from the dataset.

# In[12]:


books_data['language_code'].fillna('unknown',inplace=True)
books_data['language_code'] = books_data.groupby('authors')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# ### Now checking the data of Charles Dickens again we can see that the author of A Christmas Carol is imputed correctly

# In[13]:


charlesDickens = books_data[books_data['authors']=='Charles Dickens']
charlesDickens


# ### Now checking the values that are still marked us 'unknown'

# In[14]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Since we have 584 values still marked as unknown, we will try and impute using the title of the book just in case there are some multiple entries of the same book

# In[15]:


books_data['language_code'] = books_data.groupby('title')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# ### Now checking the shape of the dataset again

# In[16]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Now imputing the same with the image url and checking the shape again

# In[17]:


books_data['language_code'] = books_data.groupby('image_url')['language_code'].transform(lambda x: x.replace('unknown',(x.mode()[0])))


# In[18]:


unk = books_data[books_data['language_code']=='unknown']
unk.shape


# ### Now finally we were able to bring down the null values count to 267 from a count of 1000+

# In[19]:


msno.matrix(books_data)


# In[20]:


ratings_data.head()


# In[21]:


ratings_data.shape


# In[22]:


ratings_data.isnull().sum()


# In[23]:


book_tags_data.head()


# In[24]:


book_tags_data.shape


# In[25]:


book_tags_data.isnull().sum()


# In[1]:


tags_data


# In[27]:


tags_data.shape


# In[28]:


tags_data.isnull().sum()


# ## Authors

# ## Cleaning the data for multiple authors so that the authors that are comma separated can be  splitted into multiple rows. This way they can come under proper analysis.

# ### Lets start with counting the total number of books by every author

# In[29]:


books_data['authors'].value_counts()


# ### Now from the above analysis we can see that the author Dean Koontz have written 47 books. But this may not be correct as the script is picking up only those books which have only Dean Koontz as author and not the books where Dean Koontz is a co-author

# ### The below script will help us picking up values where Dean Koontz is a co author as well.

# In[30]:


DKBooks = []
books_data['authors'].apply(lambda p: DKBooks.append(p) if 'Dean Koontz' in p else [])
DKBooks


# ### So as per the actual analysis, the total books published by Dean Koontz is 64

# In[31]:


len(DKBooks)


# ### The total number of books by multiple authors in the dataset are

# ### Trying to figure out the actual number of books written by a specific author so that it can be included in analysis

# In[32]:


auth_books = []
books_data.authors.apply(lambda p: auth_books.append(p) if ',' in p else [])
auth_books[:20]


# In[33]:


len(auth_books)


# ### Splitting the data with comma separated values and then removing the actual author column and joining with the new splitted column

# In[34]:


splittedData = books_data['authors'].str.split(',').apply(Series, 1).stack()


# In[35]:


splittedData.index = splittedData.index.droplevel(-1)


# In[36]:


splittedData.name = 'authors'


# In[37]:


del books_data['authors']


# In[38]:


books_data=books_data.join(splittedData)


# In[39]:


books_data[books_data['best_book_id']==843]


# In[40]:


books_data.head()


# In[ ]:





# ### Now as we can see that the authors data in the dataset is cleaned and now we have authors column splitted into multiple rows so that we have only one author per row.
# 
# ### And this is proved by the following scripts.

# In[41]:


auth_books = []
books_data.authors.apply(lambda p: auth_books.append(p) if ',' in p else [])
auth_books[:20]


# In[42]:


len(auth_books)


# ## Data Exploratory Analysis

# ### Understanding the outliars using box plots

# ### Drawing a box plot to understand the spread of average ratings.

# In[43]:


plt.figure(figsize=(8,4))
sns.boxplot(data=books_data['average_rating'])


# ### Drawing a box plot for understanding the spread of publication year.

# In[44]:


plt.figure(figsize=(8,4))
sns.boxplot(data=books_data['original_publication_year'])


# ### Drawing a scatter plot for understanding the distribution of ratings_5 vs average_ratings

# In[45]:


plt.figure(figsize=(28,10))
sns.lmplot(x='average_rating', y='ratings_5', data=books_data)


# ### Sorting data according to the average ratings

# In[46]:


sortedData = books_data[books_data['ratings_count']>=1500]
sortedData = sortedData.sort_values('average_rating', ascending=False)
sortedData.head()


# In[47]:


plt.figure(figsize=(15,12))
ax = sns.barplot(x=sortedData['average_rating'].head(15), y=sortedData['title'].head(15), data=sortedData)
plt.title('Best ' + str(15) + ' books by ' + 'average_rating'.replace('_',' ').capitalize(), weight='bold')
plt.xlabel('Score of ' + 'average_rating')
plt.ylabel('Book Title')


# ## Count of books written in different languages

# In[48]:


langCounts = pd.DataFrame(books_data['language_code'].value_counts())
langCounts.columns = ['Total Counts']
langCounts = langCounts.sort_values('Total Counts', ascending=False)
langCounts


# In[49]:


len(langCounts)


# In[50]:


plt.figure(figsize=(16,8))
plt.title("Books Released Language Wise")
plt.bar(x=langCounts.index,height='Total Counts', data=langCounts);


# In[51]:


langCounts = langCounts.drop(["en-US", "en-GB", "eng", "en-CA"])


# In[52]:


plt.figure(figsize=(16,8))
plt.title("Books Released Language Wise (Excluding English)")
plt.bar(x=langCounts.index,height='Total Counts', data=langCounts);


# In[53]:


get_ipython().system('jupyter nbconvert data_pre*.ipynb --to python')


# ## Adding Summary Dataset

# In[54]:


books_data.shape


# In[56]:


data = []

with open("../data/booksummaries.txt", 'r',encoding='utf-8') as f:
    reader = csv.reader(f, dialect='excel-tab')
    for row in tqdm(reader):
        data.append(row)


# In[57]:


book_id = []
book_name = []
summary = []
genre = []

for i in tqdm(data):
    book_id.append(i[0])
    book_name.append(i[2])
    genre.append(i[5])
    summary.append(i[6])

books = pd.DataFrame({'book_id': book_id, 'book_name': book_name,
                       'genre': genre, 'summary': summary})
books.head(2)


# In[58]:


books.rename(columns = {'book_name':'title'}, inplace = True)


# In[59]:


books.drop(books[books['genre']==''].index, inplace=True)
books[books['genre']=='']


# In[60]:


genres = []
for i in books['genre']:
    genres.append(list(json.loads(i).values()))
books['genre_new'] = genres


# In[61]:


all_genres = sum(genres,[])
len(set(all_genres))


# In[62]:


def clean_summary(text):
    text = re.sub("\'", "", text)
    text = re.sub("[^a-zA-Z]"," ",text)
    text = ' '.join(text.split())
    text = text.lower()
    return text


# In[63]:


# books_data['title'] = books_data['title'].apply(lambda x: clean_summary(x))
books_data.head(2)


# In[64]:


books['clean_summary'] = books['summary'].apply(lambda x: clean_summary(x))
books.head(2)


# In[65]:


books['title'] = books['title'].apply(lambda x: clean_summary(x))
books.head(2)


# In[ ]:





# In[66]:


merged_df=books_data.merge(books, on='title', how='left')


# In[67]:


merged_df.head(20)


# In[68]:


merged_df.shape


# In[69]:


merged_df.isnull().sum()


# In[70]:


books_data['summary']=''


# In[71]:


dummy_data=books_data.head(10)


# In[72]:


# split = dummy_data['isbn13'].str.split(',', 1, expand=True)
dummy_data['isbn13'] = dummy_data['isbn13'].astype(int)
dummy_data['summary']=''


# In[73]:


API_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:"


# In[74]:


df_isbn['isbn'] = df_isbn.head(10)
df_isbn


# In[75]:


for row in tqdm(df_isbn):
    req = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + ""
    res = urllib.request.urlopen(req)
    result = json.loads(res.read().decode('utf-8'))
    print(result['items'][0]['volumeInfo']['description'])
    
headers("={"Content-Type":"text"}")


# In[76]:


books_data= books_data.dropna()

books_data['isbn13'] = books_data['isbn13'].astype(int)


# In[77]:


for index, row in books_data.iterrows():
    if row['summary'] == '':
        print(row['title'])
        req = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(row['isbn13'])
        res = urllib.request.urlopen(req)
        result = json.loads(res.read().decode('utf-8'))
        if 'items' in result:
            time.sleep(.5)
            if 'volumeInfo' in result['items'][0]:
                if 'description' in result['items'][0]['volumeInfo']:
                    books_data.at[index , 'summary'] = result['items'][0]['volumeInfo']['description']
                else:
                    books_data.at[index , 'summary']=np.nan
            else:
                books_data.at[index , 'summary']=np.nan
#                 row['summary']=result['items'][0]['volumeInfo']['description']
                
        else:
            books_data.at[index , 'summary']=np.nan


# In[ ]:


while True:
    try:
        for index, row in books_data.iterrows():
            if row['summary'] == '':
#                 print(row['title'])
                req = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(row['isbn13'])
                res = urllib.request.urlopen(req)
                result = json.loads(res.read().decode('utf-8'))
                if 'items' in result:
#                     time.sleep(1)
                    if 'volumeInfo' in result['items'][0]:
                        if 'description' in result['items'][0]['volumeInfo']:
                            print(row['title'])
                            books_data.at[index , 'summary'] = result['items'][0]['volumeInfo']['description']
                        else:
                            books_data.at[index , 'summary']=np.nan
                    else:
                        books_data.at[index , 'summary']=np.nan
        #                 row['summary']=result['items'][0]['volumeInfo']['description']

                else:
                    books_data.at[index , 'summary']=np.nan
    except HTTPError as err:
        print("stuck")


# In[ ]:


books_data.to_csv()


# In[ ]:





# In[ ]:


books_data[books_data['summary']==''].shape


# In[ ]:


books_data[books_data['summary']==NaN].shape


# In[ ]:


books_data.head(10)


# In[ ]:


for index, row in dummy_data.iterrows():
    req = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(row['isbn13'])
#     res = urllib.request.urlopen(req, headers={"Content-Type":"text"})
    res=requests.get(req, headers={"Content-Type":"text"})
    print(res)


# In[ ]:


http = urllib3.PoolManager()
for index, row in dummy_data.iterrows():
    time.sleep(.5)
    req = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + str(row['isbn13'])
    r = http.request('GET', req)
    result = r.data.decode("utf-8")
    print(result)


# In[ ]:


if 'items' in result:
    time.sleep(.5)
    if 'volumeInfo' in result['items'][0]:
        if 'description' in result['items'][0]['volumeInfo']:
            books_data.at[index , 'summary'] = result['items'][0]['volumeInfo']['description']
#                 row['summary']=result['items'][0]['volumeInfo']['description']
            
else:
    books_data.at[index , 'summary']=np.nan

