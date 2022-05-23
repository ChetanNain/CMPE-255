#!/usr/bin/env python
# coding: utf-8

# # Data Visualization:

# Now make some pretty plots to visualize the data.

# # Importing Libraries
# 

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import plotly_express  as px
import warnings
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud,STOPWORDS


warnings.filterwarnings('ignore')


# # Importing Datasets

# In[2]:


vamsidhar_books_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/books_data.csv')
vamsidhar_ratings_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/books_ratings_data.csv')
vamsidhar_book_tags_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/book_tags_data.csv')
vamsidhar_tags_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/tags_data.csv')


# ### Books Data

# In[3]:


print(vamsidhar_books_data.shape)


# In[4]:


print(list(vamsidhar_books_data.columns))


# In[5]:


vamsidhar_books_data.head()


# In[6]:


vamsidhar_books_data.dtypes


# In[7]:


vamsi_important_columns = ['title','authors','average_rating','ratings_count','work_text_reviews_count']


# ## Ratings Dataset

# In[8]:


vamsidhar_ratings_data.shape


# ## Ratings data

# In[9]:


print(vamsidhar_ratings_data.shape)
print(list(vamsidhar_ratings_data.columns))


# In[10]:


vamsidhar_ratings_data.head()


# ## Ratings Distribution
# 

# In[11]:


plt.rc("font", size = 15)
vamsidhar_ratings_data.rating.value_counts(sort = False).plot(kind = 'bar')
plt.title('Rating Distribution')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.plot()
plt.savefig("Ratings Distribution.jpg", bbox_inches = "tight", dpi = 100)


# In[ ]:





# # 1. Data Visualization

# ### Sorting data according to the average ratings

# In[12]:


sortedData = vamsidhar_books_data[vamsidhar_books_data['ratings_count']>=1500]
sortedData = sortedData.sort_values('average_rating', ascending=False)
print(sortedData)
# sortedData.head()


# In[ ]:





# ### 1.1 Top Rated Books
# 
#     
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and visualize Top rated books in the dataset.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
#     -------------------
#     
#    
#     
# 

# There is a clear visual representation of top rated books according to the average ratings provided on X-axis, which ranges from 0-5 only.

# In[13]:


def top_rated_books(books_data):
    top_rated_books = books_data.sort_values('average_rating', ascending=False)
    df_top_rated = top_rated_books[:15]
    fig = px.bar(df_top_rated, x="average_rating", y="original_title", title='Top Rated Books and Their Ratings')
    fig.update_layout(xaxis_range=[0,5])
    fig.show()
top_rated_books(vamsidhar_books_data)
#vamsidhar_ratings_data


# ## 1.2 Popular Book

# In[14]:


top_popular = vamsidhar_books_data.sort_values('ratings_count', ascending=False)
fifty_top_popular = top_popular[:50]
fig = px.bar(fifty_top_popular, x="ratings_count", y="original_title", title='Top Popular Books', orientation='h', color='original_title',
             width=1500, height=700)
fig.show()


# In[15]:


fig = px.treemap(fifty_top_popular, path=['original_title'], values='ratings_count',title='Popular Books', width=1000, height=700)
fig.show()


# In[ ]:





# ### 1.3 Best 15 books by Average rating

# In the below bar graph, the bars are proportional to the values they represent, and the data is visualized using sns barplots. Average score has been taken on the X-axis and book title has been taken on the Y-axis. A visual representation of the bars is created by comparing both Average Score and book titles.

# In[16]:


plt.figure(figsize=(10,10))
ax = sns.barplot(x=sortedData['average_rating'].head(15), y=sortedData['title'].head(15), data=sortedData)
plt.title('Best ' + str(15) + ' books by ' + 'average_rating'.replace('_',' ').capitalize(), weight='bold')
plt.xlabel('Score of ' + 'average_rating')
plt.ylabel('Book Title')    


# ### 1.4 Top rated books(average rating according to number of users)
# 

# We may observe many books with average rating equal to 10 and 0 as many of the books are rated only once, hence this can't show us a good visualisation
# 
# 

# In[17]:


top_rated_books = vamsidhar_books_data[['title','average_rating']]
top_rated_books = top_rated_books.groupby('title', as_index=False)['average_rating'].mean()
top_rated_books = top_rated_books.sort_values('average_rating',ascending=False).reset_index()
top_rated_books = top_rated_books[['title','average_rating']]

top_rated_books.head()


# In[18]:


top_rated_books.tail()


# ### 1.5 Average Ratings Distribution
#     
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and visualize Average ratings for the books in the dataset.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
#     -------------------
#     
#    
#    

# In this case, I have plotted average_rate from book data and represented numeric data as bars by                   dividing it into bins and visually representing each bin. Here it is very handy for quickly changing               the property of the bins or changing the display

# In[19]:


def avg_rating(vamsidhar_books_data):
    plt.figure(figsize=(10,5))
    vamsidhar_books_data["average_rating"].hist()
    display()
avg_rating(vamsidhar_books_data)


# 

# In[20]:


vamsidhar_books_data


# # 2. Authors

# ### 2.1 Filter Authors 
# 

# In[21]:


vamsidhar_books_data.authors.value_counts()


# In[22]:


a = []
vamsidhar_books_data.authors.apply(lambda x: a.append(x) if ',' in x else [])
a[:10]


# In[23]:


print('Number of books with multi-authors is {}.'.format(len(a)))


# In[ ]:





# With Authors, it's difficult to make analysis on them because the goodreads data not just include the author(s), but also sometimes include the illustarator, translator and so on (separated by ',').
# 
# So it wouldn't be easy to know the number of books for each author as we can notice above.
# 
# So I thought in 3 solutions (and their drawbacks):
# 
# We can simply just take the first author for each book and remove the rest
# Problem: there are books with co-authors, in addition, the main author doesn't always come in the 1st place (as above).
# For books with multi-authors, we can sort them according to their number of occurrences in the whole data and just keep the most frequent one.
# Problem: again, there are books with co-authors
# We can scrape data for authors (if possible) from goodreads and remove the unwanted ones.
# Problem: it will cost time and effort
# So I decided to try playing with the recent data as possible, and maybe someone like the illustrator affect the book rating.

# In[24]:


authors_list = vamsidhar_books_data['authors'].apply(lambda x: [a for a in x.split(', ')] if ',' in x else x)
authors_list.head()


# In[25]:


splitted_authors = authors_list.apply(lambda x: pd.Series(x)).stack().reset_index(level=1, drop=True)
splitted_authors.name = 'authors'
splitted_authors.head()


# In[26]:


vamsi_df_edited_authors = vamsidhar_books_data[vamsi_important_columns].drop('authors', axis=1).join(splitted_authors)
vamsi_df_edited_authors.head()


# In[27]:


vamsi_df_edited_authors.authors.value_counts()


# We can see now the difference as the previous largest number of books was 60 for Stephen King, now it's 98 for James Patterson.
# 
# 

# In[28]:


def vamsi_plot_authors_by(df, title, xlabel, n=15, ylabel='Author', y_size=7):
    plt.figure(figsize=(15,y_size))
    ax = sns.barplot(x=df.head(n).values, y=df.head(n).index)
    plt.title(title, weight='bold')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


# ### 2.2 Authors with Most Books 
# 

# In[29]:


authors_most_with_books = vamsi_df_edited_authors.authors.value_counts()
authors_most_with_books.head(15)


# In[30]:


vamsi_plot_authors_by(authors_most_with_books, 'Authors with most books', 'Number of Books', 30)


# ### 2.3 Top Authors
# 
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and visualize Top Authors for the books in the dataset.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
#     -------------------
#     
#   
#     
# 
# 

# Interactive Barplot between count and the authors and visualized top authors of books in the dataset in the form of bar graph.

# In[31]:


def topauthors(vamsidhar_books_data):
    top_authors = vamsidhar_books_data['authors'].value_counts().reset_index()
    top_authors.columns = ['authors', 'count']
    top_authors['authors'] = top_authors['authors']
    top_authors = top_authors.sort_values('count')
    fig = px.bar(top_authors.tail(10), x="count", y="authors", color='authors',
                 width=1000, height=700)
    fig.show()
topauthors(vamsidhar_books_data)


# In[55]:


fifty_top_authors = vamsidhar_books_data[:50]
fig = px.treemap(fifty_top_authors, path=['authors'], values='average_rating',title='Popular Authors', width=1000, height=700)
fig.show()


# ### 2.4  Percentage of Ratings According to Authors

# In[56]:


from plotly.offline import init_notebook_mode, iplot, plot


# In[57]:


data1= vamsidhar_books_data.head(20)
data1.rename(columns={'ratings_1':'R1', 'ratings_2':'R2','ratings_3':'R3','ratings_4':'R4','ratings_5':'R5'}, inplace=True)


# In[58]:


author_list= list(data1['authors'].unique())

ratings1= []
ratings2= []
for i in author_list:
    
    x = data1[data1['authors']==i]
    ratings1.append(sum(x.R1)/len(x))
    ratings2.append(sum(x.R2)/len(x))
    
f,ax = plt.subplots(figsize = (5,8))
sns.barplot(x=ratings1,y=author_list,color='green',alpha = 0.5,label='Rating1' )
sns.barplot(x=ratings2,y=author_list,color='blue',alpha = 0.5,label='Rating2' )
ax.legend(loc='lower right',frameon = True)   
ax.set(xlabel='Percentage of Ratings', ylabel='Authors',title = "Percentage of Ratings According to Authors ")
plt.show()


# In[59]:


df2004 = vamsidhar_books_data[vamsidhar_books_data.original_publication_year == 2004].iloc[:200,:]
df2005 = vamsidhar_books_data[vamsidhar_books_data.original_publication_year == 2005].iloc[:200,:]
df2003 = vamsidhar_books_data[vamsidhar_books_data.original_publication_year == 2003].iloc[:200,:]

import plotly.graph_objs as go
trace1 =go.Scatter(
                    x = data1.average_rating,
                    y = data1.R1,
                    mode = "markers",
                    name = "2004",
                    marker = dict(color = 'rgba(255, 128, 255, 0.8)'),
                    text= df2004.authors)
trace2 =go.Scatter(
                    x = data1.average_rating,
                    y = data1.R2,
                    mode = "markers",
                    name = "2005",
                    marker = dict(color = 'rgba(255, 128, 2, 0.8)'),
                    text= df2005.authors)
trace3 =go.Scatter(
                    x = data1.average_rating,
                    y = data1.R3,
                    mode = "markers",
                    name = "2003",
                    marker = dict(color = 'rgba(0, 255, 200, 0.8)'),
                    text= df2003.authors)
data = [trace1, trace2, trace3]
layout = dict(
              xaxis= dict(title= 'Average Ratings',ticklen= 9,zeroline= False),
              yaxis= dict(title= 'Ratings',ticklen= 9,zeroline= False),
              title = "Ratings and Avarage Ratings of 2004/2005/2006"
             )
fig = dict(data = data, layout = layout)
iplot(fig)


# In[ ]:





# ### 2.5 Number of Authors Ratings Rates
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and returns the Number of Authors Ratings Rates for year 2015 and 2016.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
# 
# 
# 

# In[60]:


def getpiechart(vamsidhar_books_data):
    df = vamsidhar_books_data[vamsidhar_books_data.original_publication_year == 2015].iloc[:7,:]
    pie1 = df.ratings_1
    df1 = vamsidhar_books_data[vamsidhar_books_data.original_publication_year == 2016].iloc[:7,:]
    pie2 = df1.ratings_1
    labels = df.authors.value_counts().index

    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=pie1, name="Number Of Authors Rates"),
                  1, 1)
    fig.add_trace(go.Pie(labels=labels, values=pie2, name="Number Of Authors Rates"),
                  1, 2)
    fig.update_traces(hole=.45, hoverinfo="label+percent+name")
    fig.update_layout(
        height=800, width=800,
        annotations=[dict(text='2015', x=0.175, y=0.5, font_size=14, showarrow=False),
                     dict(text='2016', x=0.82, y=0.5, font_size=14, showarrow=False)])
    fig.show()
getpiechart(vamsidhar_books_data)


# ### 2.6 Wordcloud of Authors
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and returns the wordcloud of author.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
# 

# ### Visualising most frequent words in Author

# Creating string variables for authors and original_title, also creating a function to plot WordCloud()

# In[63]:


stop_words=set(STOPWORDS)
author_string = " ".join(vamsidhar_books_data['authors'])
title_string = " ".join(vamsidhar_books_data['original_title'])


# In[68]:


vamsidhar_books_data.head()


# In[64]:


def wordcloud(string):
    wc = WordCloud(width=800,height=500,mask=None,random_state=21, max_font_size=110,stopwords=stop_words).generate(string)
    fig=plt.figure(figsize=(16,8))
    plt.axis('off')
    plt.imshow(wc)


# Displaying most frequent words in author names
# 
# 

# In[65]:


wordcloud(author_string)


# Displaying most frequent words in title names
# 

# In[66]:


wordcloud(title_string)


# ## 3. Number of books in each year
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and returns the histogram plot to visualize the number of books published each year.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
# 
# 

# In[43]:


# Visualising Explicit Rating Countsdef get_histplot(books_data):
def get_histplot(vamsidhar_books_data):   
    sns.histplot(x="original_publication_year", data=vamsidhar_books_data, bins=1000)
    plt.xlim(1900,2020);
get_histplot(vamsidhar_books_data)


# # 4. Language

# The books.csv contains information on the languages of the books, as you might have noticed.Goodreads is an english language site, so this is interesting.There are some books in other languages in the dataset.There are often multiple editions of a book (both in the same language and in different languages).According to this dataset, the most popular edition was included, which for some books is their original language.

# In[44]:


lang_counts = pd.DataFrame(vamsidhar_books_data['language_code'].value_counts())
lang_counts.columns = ['counts']
lang_counts


# In[45]:


plt.figure(figsize=(16,8))
plt.title("Number of Books released in a specific Language (English included).", weight='bold')
plt.bar(x=lang_counts.index,height='counts', data=lang_counts);


# In[46]:


lang_counts = lang_counts.drop(["en-US", "en-GB", "eng", "en-CA"])


# Number of Books released in a specific Language (English excluded)

# In[47]:


plt.figure(figsize=(16,8))
plt.title("Number of Books released in a specific Language (English excluded).", weight='bold')
plt.bar(x=lang_counts.index,height='counts', data=lang_counts);


# In[ ]:





# # 5. Treemap
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and visualize dataset in form of Treemap.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
#     -------------------
#     
#     

# The following treemap displays hierarchical data as nested rectangles. Each group is represented by a rectangle, whose area varies according to its value.

# In[48]:


def get_treemap(vamsidhar_books_data):
    
    dropna= vamsidhar_books_data.dropna()
    fig = px.treemap(dropna, path=['original_publication_year','language_code', "average_rating"],
                      color='average_rating')
    fig.show()
get_treemap(vamsidhar_books_data)


# # 6. Heatmap
#     Author : Vamsidhar
#     
#     This function takes in a dataframe and returns the correlation between all the columns.
#     
#     Params:
#     -------------------
#     input: books_data
#            =>dataframe
# 

# In[49]:


heatmap1= vamsidhar_books_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/books_data.csv')
heatmap2= vamsidhar_ratings_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/books_ratings_data.csv')
heatmap3= vamsidhar_book_tags_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/book_tags_data.csv')
heatmap4= vamsidhar_tags_data = pd.read_csv('/Users/vamsidharreddy/CMPE-255-Final-Project/data/book_tags_data.csv')


# In[50]:


vamsidhar_df = heatmap1.drop(['id','book_id','best_book_id','work_id','isbn13'],axis=1)


# In[51]:


vamsidhar_df


# In[52]:


def get_heatmap(vamsidhar_df):
    f,ax = plt.subplots(figsize=(10,10))
    sns.heatmap(vamsidhar_df.corr(), annot=True, linewidths=0.6,linecolor="black", fmt= '.1f',ax=ax)
    plt.show() 
get_heatmap(vamsidhar_df)


# In[ ]:





# In[53]:


get_ipython().system('jupyter nbconvert Data*.ipynb --to python')


# In[ ]:




