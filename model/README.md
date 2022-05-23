# Recommendation System Models
A recommendation system is a subclass of Information filtering Systems that seeks to predict the rating or the preference a user might give to an item. .
Recommender systems are really critical in some industries as they can generate a huge amount of income when they are efficient or also be a way to stand out significantly from competitors.
The above implemented models cover both paradigms of recommendation system: Collaborative and Content based filtering.


## Collaborative filtering:
Collaborative methods for recommender systems are methods that are based solely on the past interactions recorded between users and items in order to produce new recommendations. These interactions are stored in the so-called “user-item interactions matrix”.
The main advantage of collaborative approaches is that they require no information about users or items and, so, they can be used in many situations. Moreover, the more users interact with items the more new recommendations become accurate: for a fixed set of users and items, new interactions recorded over time bring new information and make the system more and more effective.

The main idea that rules collaborative methods is that these past user-item interactions are sufficient to detect similar users and/or similar items and make predictions based on these estimated proximities.

It is further divided into two subparts:
* 1 User - User:
  In order to make a new recommendation to a user, user-user method roughly tries to identify users with the most similar “interactions profile” (nearest neighbours) in order to suggest items that are the most popular among these neighbours (and that are “new” to our user). This method is said to be “user-centred” as it represent users based on their interactions with items and evaluate distances between users.
    <image here user_id = 40>
* 2 Item - Item:
  To make a new recommendation to a user, the idea of item-item method is to find items similar to the ones the user already “positively” interacted with. Two items are considered to be similar if most of the users that have interacted with both of them did it in a similar way. This method is said to be “item-centred” as it represent items based on interactions users had with them and evaluate distances between those items.
  
  <image here item>
    
## Content Based filtering:
In content based methods, the recommendation problem is casted into either a classification problem (predict if a user “likes” or not an item) or into a regression problem (predict the rating given by a user to an item). In both cases, we are going to set a model that will be based on the user and/or item features at our disposal (the “content” of our “content-based” method).
The content-based approach uses additional information about users and/or items. This filtering method uses item features to recommend other items similar to what the user likes and also based on their previous actions or explicit feedback. If we consider the example for a books recommender system, the additional information can be, the age, the sex, the job or any other personal information for users as well as the category, the main character, the writing style, length or other characteristics for the books i.e the items.
   
The main idea of content-based methods is to try to build a model, based on the available “features”, that explain the observed user-item interactions. 

### Limitations

Basis of the findings, our content-based filtering approach has the following limitations:
Our recommender chose some films that a person searching for 'my sunshine away' titles would most likely find offensive. To enhance our system, we may replace TF-IDF with word counts and investigate alternative similarity scores.
As of now, our algorithm solely evaluates the storyline summaries of each books. 
As of now, our algorithm simply evaluates the book summaries of each book. Other factors, such as writers and genre, will almost certainly help us identify comparable movies.
Our present approach only recommends movies that have comparable properties. As a result, our recommender is missing books from different genres that the user may love. To overcome this, we'd have to employ collaborative filtering, but our dataset didn't include any user information.
 
<Insert similar summary image here>
  
## Hybrid Approach:
It is evident that both the techniques are equally good and complement each other. We explored and studied recommendation technologies based on content filtering and user collaborative filtering and propose a hybrid recommendation algorithm based on content and user collaborative filtering. This method not only makes use of the advantages of content filtering but also can carry out similarity matching filtering for all items, especially when the items are not evaluated by any user, which can be filtered out and recommended to users, thus avoiding the problem of early level. 
 
 At the same time, this method also takes advantage of the advantages of collaborative filtering. When the number of users and evaluation levels are large, the user rating data matrix of collaborative filtering prediction will become relatively dense, which can reduce the sparsity of the matrix and make collaborative filtering more accurate. In this way, we will try to improve the system performance through the integration of the two.
