# Data Preprocessing

The process of converting raw data into a comprehensible format is known as data preparation. We can't deal with raw data, thus this is a key stage in data mining. Before using machine learning or data mining methods, make sure the data is of good quality.

## What is the significance of data preprocessing?

The purpose of data preprocessing is to ensure that the data is of good quality. The following criteria can be used to assess quality:

**Accuracy**: To determine whether or not the data entered is correct.

**Checking for completeness**: To see if the data is accessible or not.

**Consistency**: Check for consistency by seeing if the same data is retained in all of the areas that match or don't match.

**Updatable**: Data should be updated on a regular basis.

**Trustworthiness**: The data should be reliable.

**Data interpretability**: The data's ability to be comprehended.

## 1. Checking for null values and replacing with suitable values

Using fillna(), replace(), and interpolate() to fill in missing values.
We employ the fillna(), replace(), and interpolate() functions to fill null values in datasets. 
These functions substitute NaN values with their own values. All of these functions aid in the filling of null values in DataFrame datasets. 
The Interpolate() method is used to fill NA values in a dataframe, but instead of hard-coding the value, it employs various interpolation techniques to fill the missing values.


<p>
    <img src="./images/null value dist.png" width="1000" height="600" />
</p>

## In our data set too we had 1000+ null values in the language_code column. So we tried to impute these null values. Applying the lambda function to replace the null values with the languages of the author who have written any other book in the dataset. We can pick the language code from any other book written by the author and can replace the null values. 

<p>
    <img src="./images/Lang with null.png" width="1000" height="600" />
</p>

## Just like we have done for Charles Dickens, The book with title 'The Christmas Carol' was missing the language code in the above dataset, but from the dataset we know Charles Dickens has written multiple books in English. 

<p>
    <img src="./images/CD with NA.png" width="1000" height="600" />
</p>

## So we will impute the values and replace the null values with the language code of the mode value obtained. 

<p>
    <img src="./images/CD without Na.png" width="1000" height="600" />
</p>

## This way  we were able to retrieve around 80% of the missing values from the dataset.


## 2. Detecting Outliers: 
Outliers are extreme results that differ from previous data observations; they may suggest measurement variability or experimental mistakes. To put it another way, an outlier is an observation that deviates from a sample's main trend.

Outliers were treated using the following methods:

 a.) Remove the outliers 
 
 b.) Substitute with the median or a fixed value
 
 
 ### The below screenshot is the box plot for the average ratings.
 
 <p>
    <img src="./images/box plot.png" width="800" height="600" />
</p>
 
 
  ### The below screenshot is the box plot for the year of publication of various books.
 
  <p>
    <img src="./images/box plot 2.png" width="800" height="600" />
</p>
 
 
 ## 3. Organizing the data by getting it into proper format so that it can be used for analysis. 
 
 ## In the dataset we have to clean the data for multiple authors so that the authors that are comma separated can be splitted into multiple rows. This way they can come under proper analysis.
 
  <p>
    <img src="./images/Inital Author Count.png" width="1000" height="600" />
</p>


### Now from the above analysis we can see that the author Dean Koontz have written 47 books. But this may not be correct as the script is picking up only those books which have only Dean Koontz as author and not the books where Dean Koontz is a co-author.
  <p>
    <img src="./images/DK list of book.png" width="1000" height="600" />
</p>

  <p>
    <img src="./images/DK 64 count.png" width="1000" height="600" />
</p>

### So we will be doing the below operations to get the authors data into individual rows rather than in the form of comma separated values in a single cell.

  <p>
    <img src="./images/author comma sep.png" width="1000" height="600" />
</p>


### By the above operation we were able to get the right count of Dean Koontz books and also were able to bring the data in the right format. This format of data will help us do proper analysis related to authors.

  <p>
    <img src="./images/cleaned author.png" width="1000" height="400" />
</p>
