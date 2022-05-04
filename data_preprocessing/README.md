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


## 2. Detecting Outliers: 
Outliers are extreme results that differ from previous data observations; they may suggest measurement variability or experimental mistakes. To put it another way, an outlier is an observation that deviates from a sample's main trend.

Outliers were treated using the following methods:
 a.) Remove the outliers 
 b.) Substitute with the median or a fixed value
 
 
 
