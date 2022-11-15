from flask import Flask, Response, jsonify
import csv
from operator import itemgetter
import pandas as pd

app = Flask(__name__)

# Lists that are going to contain the data
links = []
movies = []
ratings = []
tags = []

# open links.csv file, read it and save it to the links list
with open('data/links.csv', mode ='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        links.append(lines)

# open ratings.csv file, read it and save it to the ratings list
with open('data/ratings.csv', mode ='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        ratings.append(lines)

# open tags.csv file, read it and save it to the tags list
with open('data/tags.csv', mode ='r') as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        tags.append(lines)

# open movies.csv file, read it and save it to the movies list
with open('data/movies.csv', mode ='r', encoding="utf8") as file:
    csvFile = csv.reader(file)
    for lines in csvFile:
        movies.append(lines)

# Make an average of the ratings for each movie
def make_average_ratings():
    # Changee the type of the movieId and userId to int instead of string
    ratings_int = [[int(rating[0]), int(rating[1]), rating[2], rating[3]] for rating in ratings[1:]]
    # Add the columns names
    ratings_int.insert(0, ratings[0])
    # Sort the ratings by movies instead of by users
    ratings_movies_ordered = sorted(ratings_int[1:], key=itemgetter(1))

    # Initialize variables
    movie_id = ratings_movies_ordered[0][1]
    prev_movie_id = ratings_movies_ordered[0][1]
    cnt = 0
    sum_ratings = 0
    ratings_averages = []

    # Go through each rating
    for rating in ratings_movies_ordered:
        movie_id = rating[1]
        # Check if movie has changed
        if prev_movie_id != movie_id:
            # If yes, compute average, save it, and reset variables
            avg_rating = sum_ratings / cnt
            ratings_averages.append([prev_movie_id, avg_rating])
            cnt = 0
            sum_ratings = 0
            prev_movie_id = movie_id
        # Count the current movie rating
        cnt += 1
        sum_ratings += float(rating[2])
    # Add the last rating to the container
    avg_rating = sum_ratings / cnt
    ratings_averages.append([prev_movie_id, avg_rating])
    return ratings_averages

avg_ratings = make_average_ratings()
# Add columns names
avg_ratings.insert(0, ['movieId', 'avg_rating'])

# make a dataframe for the tags, and change the type of userId and movieId
df_tags = pd.DataFrame(tags)
df_tags.columns = df_tags.iloc[0]
df_tags = df_tags[1:]
df_tags[['userId', 'movieId']] = df_tags[['userId', 'movieId']].apply(pd.to_numeric)

# make a dataframe for the ratings
df_avg_ratings = pd.DataFrame(avg_ratings)
df_avg_ratings.columns = df_avg_ratings.iloc[0]
df_avg_ratings = df_avg_ratings[1:]

# Function to make a table containing all the necessary information:
# movie name, links, tags, average rating...
def make_whole():
    # Initialize with an empty list
    whole_table = []
    # Go through each movie
    for index, movie in enumerate(movies[1:]):
        # Initialize variables
        rating_movie = ['NA']
        tags_movie = ['']
        movie_id = movie[0]
        # Get all the tags given to this movie
        tags_movie = list(df_tags.loc[df_tags['movieId'] == int(movie_id) ]['tag'].values)
        # Get the average rating of this movie
        rating_movie = df_avg_ratings[df_avg_ratings['movieId'] == int(movie_id)]['avg_rating'].values
        if rating_movie.size == 0:
            rating_movie = ['NA']
        else:
            rating_movie = [str(rating_movie[0])]
        # Add the information to the table
        whole_table.append(movie + links[index+1] + rating_movie + [tags_movie])
    return whole_table

whole_table = make_whole()

# The only endpoint used gives the data with everything needed
@app.route("/whole")
def get_whole():
    response = jsonify(whole_table)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Other routes for debugging:

# @app.route("/links")
# def get_links():
#     response = jsonify(links)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route("/movies")
# def get_movies():
#     response = jsonify(movies)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route("/ratings")
# def get_ratings():
#     response = jsonify(ratings)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route("/average_ratings")
# def get_avg_ratings():
#     response = jsonify(avg_ratings)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route("/tags")
# def get_tags():
#     response = jsonify(tags)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response