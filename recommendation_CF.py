# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 18:57:12 2020

@author: shubhashish.p
"""

import pandas as pd

ratings = pd.read_csv('rating.csv')
movies_all = pd.read_csv('movie.csv')

movies = movies_all[["movieId","title"]]

#movies = df.rename(columns={"id": "movieId"}) 
#movies = movies.rename(columns={"id": "movieId"}) 

movies.info()
ratings.info()

#movies = movies.astype({"movieId":int})
ratings = pd.merge(ratings,movies)
ratings = ratings.drop(['timestamp','movieId'], axis="columns")
ratings.head()

title_group = ratings.groupby('title')['title'].count().sort_values(ascending=True).head(17000)

sss = pd.DataFrame()
sss['count'] = title_group
sss['title'] = sss.index
sss = sss.reset_index(drop=True)

ratings = pd.merge(ratings,sss)

ratings = ratings[ratings['count'] > 50]

ratings = ratings.drop(['count'], axis="columns")


#ratings = ratings.dropna(ratings['title']) 

user_ratings = ratings.pivot_table(index=['userId'],columns=['title'],values=['rating'])
user_ratings = user_ratings.dropna(thresh=10,axis=1).fillna(0);

user_ratings.head()

user_ratings.info()

item_similarity_df = user_ratings.corr(method='pearson')
item_similarity_df.columns = item_similarity_df.columns.droplevel(0)
item_similarity_df.head(50)


#item_similarity_df = pd.DataFrame()

def get_similar_movies(title,user_rating):
    similar_score = item_similarity_df[title]*(user_rating-2.5)
    similar_score = similar_score.sort_values(ascending=False)
    
    return similar_score

action_lover = [("Jab We Met (2007)",4.5),("Sholay (1975)",5),("Veer Zaara (2004)",4)]

similar_movies = pd.DataFrame()

for title,rating in action_lover:
	similar_movies = similar_movies.append(get_similar_movies(title,rating),ignore_index=True)

similar_movies
similar_movies.sum().sort_values(ascending=False)

