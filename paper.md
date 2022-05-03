---
title: Book Recommender System
date: "May 2022"
author: Lavesh Jain, Chetan Nain, Vamsidhar Reddy Menthem - San José State University

header-includes: |
  \usepackage{booktabs}
  \usepackage{caption}
---

# Abstract

People often wondered which book to read next. Reading books doesn’t come easy to everyone. Especially, if you are unsure of the book to read. Books recommendation is yet another application of the ubiquitous recommender system present all around us. These systems affect our decisions and determine what food we would like to order, which songs to listen to, which movies to watch, and even with whom we can connect on social media. The capacity of a recommender system to be comprehensive and relevant is dependent on the effective extraction of hidden patterns from the data. In this paper, book information is retrieved using data from websites like Goodreads and Google Books. The key problem identified till now is the data cleaning. Handling the missing data is most important. Statistical methods like mode and median are used to fill categorical and numerical data likewise. We plan to explore both aspects of the recommender system: collaborative and content-based. We will do a comparative study of the performance of both techniques and plan to leverage the advantages of both to create a hybrid model for better results.

# Introduction
In today’s world where the number of options available for one product is increasing and the attention span of a user is decreasing It becomes extremely difficult to retain a customer. Customer retention is key to boosting revenue. A 5% increase in customer retention can increase company revenue by 25-95%. This is where recommender systems come into the picture. Companies like Netflix invest heavily in their recommender systems to show relevant content to the user.

This project is aimed to target the interest of book readers and recommend relevant books to readers. Book reading doesn’t come easy to everyone. Most people are very peculiar about the books they read. This is well justified as it isn’t as lucid as it looks. Two books can have similar storylines but have different writing styles or two books by the same author can have similar writing styles but an entirely different plot. Two books can be same but published in two different years or one can be the latest edition of the older one with some modifications. The fact that the data have so many features to consider, makes this project further interesting. 

# Methods

We propose to build and train the recommender system model on the books data set. Recommender systems are an important class of machine learning algorithms that offer "relevant" suggestions to users. Recommender systems are generally divided into two main categories: collaborative filtering and content-based systems.

Collaborative filtering methods for recommender systems are methods that are solely based on the past interactions between users and the target items. Thus, the input to a collaborative filtering system will be all historical data of user interactions with target items. The core idea behind such systems is that the historical data of the users should be enough to make a prediction.

The class of collaborative filtering algorithms is divided into two sub-categories that are generally called memory based and model based approaches. Memory based approaches directly works with values of recorded interactions, assuming no model, and are essentially based on nearest neighbours search. Model based approaches assume an underlying “generative” model that explains the user-item interactions and tries to discover them in order to make new predictions

Unlike collaborative methods that only rely on the user-item interactions, content based approaches use additional information about users and/or items. The idea of content based methods is to try to build a model, based on the available “features”, that explain the observed user-item interactions. Content based methods suffer far less from the cold start problem than collaborative approaches: new users or items can be described by their characteristics (content) and so relevant suggestions can be done for these new entities.

# Comparisons

# Example Analysis

# Conclusions


# References
