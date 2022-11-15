from flask import Flask
from flask import Response, jsonify
import csv
from operator import itemgetter
import pandas as pd
# import numpy as np

app = Flask(__name__)

# links = {}
links = []
movies = []
ratings = []
tags = []

# opening the CSV file
with open('data/links.csv', mode ='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)
    # displaying the contents of the CSV file
    for lines in csvFile:
        links.append(lines)

with open('data/ratings.csv', mode ='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)
    # displaying the contents of the CSV file
    for lines in csvFile:
        ratings.append(lines)


with open('data/tags.csv', mode ='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)
    # displaying the contents of the CSV file
    for lines in csvFile:
        tags.append(lines)

with open('data/movies.csv', mode ='r', encoding="utf8") as file:
    # reading the CSV file
    csvFile = csv.reader(file)
    # displaying the contents of the CSV file
    for lines in csvFile:
        movies.append(lines)


def make_average_ratings():
    # Sort the ratings by movies instead of by users
    ratings_int = [[int(rating[0]), int(rating[1]), rating[2], rating[3]] for rating in ratings[1:]]
    ratings_int.insert(0, ratings[0])
    ratings_movies_ordered = sorted(ratings_int[1:], key=itemgetter(1))
    movie_id = ratings_movies_ordered[0][1]
    prev_movie_id = ratings_movies_ordered[0][1]
    cnt = 0
    sum_ratings = 0
    ratings_averages = []

    for rating in ratings_movies_ordered:
        user_id = rating[0]
        movie_id = rating[1]
        if prev_movie_id != movie_id:
            avg_rating = sum_ratings / cnt
            ratings_averages.append([prev_movie_id, avg_rating])
            cnt = 0
            sum_ratings = 0
            prev_movie_id = movie_id
        cnt += 1
        sum_ratings += float(rating[2])
    avg_rating = sum_ratings / cnt
    ratings_averages.append([prev_movie_id, avg_rating])
    return ratings_averages

avg_ratings = make_average_ratings()
avg_ratings.insert(0, ['movieId', 'avg_rating'])

df_tags = pd.DataFrame(tags)
df_tags.columns = df_tags.iloc[0]
df_tags = df_tags[1:]
df_tags[['userId', 'movieId']] = df_tags[['userId', 'movieId']].apply(pd.to_numeric)

df_avg_ratings = pd.DataFrame(avg_ratings)
df_avg_ratings.columns = df_avg_ratings.iloc[0]
df_avg_ratings = df_avg_ratings[1:]

def make_whole():
    whole_table = []
    # Make a movie card
    # movieId 
    # tags_int = [[int(tag[0]), int(tag[1]), tag[2], tag[3]] for tag in tags[1:]]
    # tags_int.insert(0, tags[0])
    # tags_movies_ordered = sorted(tags_int[1:], key=itemgetter(1))
    for index, movie in enumerate(movies[1:]):
        rating_movie = ['NA']
        tags_movie = ['']
        movie_id = movie[0]
        tags_movie = list(df_tags.loc[df_tags['movieId'] == int(movie_id) ]['tag'].values)
        # print([str(df_avg_ratings[df_avg_ratings['movieId'] == int(movie_id)]['avg_rating'])])
        rating_movie = df_avg_ratings[df_avg_ratings['movieId'] == int(movie_id)]['avg_rating'].values
        if rating_movie.size == 0:
            rating_movie = ['NA']
        else:
            rating_movie = [str(rating_movie[0])]
        # df_avg_ratings.iloc[]
        # if movie_id in avg_ratings:
        #     # 
        #     pass
            # rating_movie = avg_ratings[movie_id][1]
        # if movies has tags, add them
        # if movie has avg rating, add it
        whole_table.append(movie + links[index+1] + rating_movie + [tags_movie])
    return whole_table

whole_table = make_whole()


@app.route("/")
def hello_world():
    # response = "<p>Hello, World!</p>"
    response = Response('some data')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/links")
def get_links():
    response = jsonify(links)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/movies")
def get_movies():
    response = jsonify(movies)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/ratings")
def get_ratings():
    response = jsonify(ratings)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/average_ratings")
def get_avg_ratings():
    response = jsonify(avg_ratings)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/tags")
def get_tags():
    response = jsonify(tags)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/whole")
def get_whole():
    # Combine movies, ratings, tags, links
    response = jsonify(whole_table)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
