# CMPE-255 Team Project



| Team Members | Id | GitHub User Name  |
| ------ | ------ | ------ |
| Chetan Nain | 015761122 | ChetanNain |
| Lavesh Jain | 015017145  | Laveshjain 11 |
| Vamsidhar Reddy Menthem | 015999191 | vamsidhar18 |


# Book Recommendation System 

Reading books doesn’t come easy to everyone. Especially, if you are not sure which book to read. Whether you will like one genre or not, or wondering if the book is even worth your time. We are working on the extensive field of recommendation systems and implementing them to suggest books according to readers’ interests.
A recommendation engine is a part of the machine learning domain that offers relevant suggestions to the customer. Such algorithms are a significant part of technology organizations like Amazon, Google, and Netflix. Applications like YouTube highly rely on recommendation systems for video suggestions so that the user sticks to their websites.
In our project we will be using a supervised learning algorithm to help readers select the next best possible book to read. We intend to solve the problem of selecting a book to read by giving readers suggestions based on their reading history. 

# Data Extraction:
Collecting the information of the books published and read over the world is a challenge in itself given the volume of data available. Goodreads is one of the popular websites among readers to review and rate the books they have read. For the purpose of this project, we are utilizing the API by Goodreads to collect the required data. The data consists of information about books like Title, Author, Date published, Genre, User ratings, Reviews, etc 
We are going to extract the data about the available books and store it in a csv file. We plan to preprocess and clean the data before carrying out any analysis on it. We assume the data to be noisy and incomplete. We are planning to use statistical data cleaning techniques like mean, median, etc to fill out the incomplete data. Techniques like box plot can be used to identify outliers.   
Recommendation systems can be divided into two categories: content-based and collaborative. In general, recommendation systems that use a content-based (CB) approach suggest things to a user that are comparable to those the user has previously favored. Collaborative filtering (CF) recommendation systems, on the other hand, forecast users' preferences by examining user relationships and item interdependencies and extrapolating new linkages from them. 
In our solution we will be using Collaborative Filtering to recommend user books to select from and on top of it we are planning to do clustering of books to divide them into sections and present data to a user section wise.
Ultimately, at the end, after achieving the desired results we will like to incorporate the hybrid approach in which we will try to leverage the deep learning to merge content based and collaborative filtering. This approach will help us in learning much fine grained interactions between the reader and books. 

# Source Dataset:
The dataset we are using has data for http://www2.informatik.uni-freiburg.de/~cziegler/BX/ 

| Feature Name | Type | Description |
| ------ | ------ |------ |
| User-ID | Numerical | Costumer_User_ID |
| ISBN | Numerical  | Book_Number |
| Book-Rating | Numerical | Book_Rating|

#Numerical Variables:
User-ID
ISBN
Book-Rating

#Methodology:
Problem Type:  Multi Classification, Regression  (Supervised Learning)
Algorithms: Collaborative Filtering



