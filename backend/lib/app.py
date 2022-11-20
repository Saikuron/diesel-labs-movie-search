from flask import Flask, jsonify
import csv
from operator import itemgetter
import pandas as pd

app = Flask(__name__)

# open file, read it and return its content
def open_file(file_name):
    result = []
    with open(file_name, mode ='r', encoding="utf8") as file:
        csvFile = csv.reader(file)
        for lines in csvFile:
            result.append(lines)
    return result

# Lists that are going to contain the data
links = open_file("data/links.csv")
movies = open_file("data/movies.csv")
ratings = open_file("data/ratings.csv")
tags = open_file("data/tags.csv")

# Make a list with just movies names for autocomplete
whole_names = [movie[1] for movie in movies[1:]]
whole_names = list(set(whole_names))

# Make an average of the ratings for each movie
def make_average_ratings(all_ratings):
    # Changee the type of the movieId and userId to int instead of string
    ratings_int = [[int(rating[0]), int(rating[1]), rating[2], rating[3]] for 
                    rating in all_ratings[1:]]
    # Add the columns names
    ratings_int.insert(0, all_ratings[0])
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

avg_ratings = make_average_ratings(ratings)
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
        tags_movie = list(df_tags.loc[df_tags['movieId'] == 
            int(movie_id)]['tag'].values)
        # Get the average rating of this movie
        rating_movie = df_avg_ratings[df_avg_ratings['movieId'] == 
            int(movie_id)]['avg_rating'].values
        if rating_movie.size == 0:
            rating_movie = ['NA']
        else:
            rating_movie = [str(rating_movie[0])]
        # Add the information to the table
        whole_table.append(movie + links[index+1] + rating_movie + [tags_movie])
    return whole_table

whole_table = make_whole()

# Tables used to have a smaller dataset for debugging purpose
sample_table = [["1","Toy Story (1995)","Adventure|Animation|Children|Comedy|Fantasy","1","0114709","862","3.9209302325581397",["pixar","pixar","fun"]],["2","Jumanji (1995)","Adventure|Children|Fantasy","2","0113497","8844","3.4318181818181817",["fantasy","magic board game","Robin Williams","game"]],["3","Grumpier Old Men (1995)","Comedy|Romance","3","0113228","15602","3.2596153846153846",["moldy","old"]],["4","Waiting to Exhale (1995)","Comedy|Drama|Romance","4","0114885","31357","2.357142857142857",[]],["5","Father of the Bride Part II (1995)","Comedy","5","0113041","11862","3.0714285714285716",["pregnancy","remake"]],["6","Heat (1995)","Action|Crime|Thriller","6","0113277","949","3.946078431372549",[]],["7","Sabrina (1995)","Comedy|Romance","7","0114319","11860","3.185185185185185",["remake"]],["8","Tom and Huck (1995)","Adventure|Children","8","0112302","45325","2.875",[]],["9","Sudden Death (1995)","Action","9","0114576","9091","3.125",[]],["10","GoldenEye (1995)","Action|Adventure|Thriller","10","0113189","710","3.496212121212121",[]]]#,["11","American President, The (1995)","Comedy|Drama|Romance","11","0112346","9087","3.6714285714285713",["politics","president"]],["12","Dracula: Dead and Loving It (1995)","Comedy|Horror","12","0112896","12110","2.4210526315789473",[]],["13","Balto (1995)","Adventure|Animation|Children","13","0112453","21032","3.125",[]],["14","Nixon (1995)","Drama","14","0113987","10858","3.8333333333333335",["politics","president"]],["15","Cutthroat Island (1995)","Action|Adventure|Romance","15","0112760","1408","3.0",[]],["16","Casino (1995)","Crime|Drama","16","0112641","524","3.926829268292683",["Mafia"]],["17","Sense and Sensibility (1995)","Drama|Romance","17","0114388","4584","3.7761194029850746",["Jane Austen"]],["18","Four Rooms (1995)","Comedy","18","0113101","5","3.7",[]],["19","Ace Ventura: When Nature Calls (1995)","Comedy","19","0112281","9273","2.727272727272727",[]],["20","Money Train (1995)","Action|Comedy|Crime|Drama|Thriller","20","0113845","11517","2.5",[]],["21","Get Shorty (1995)","Comedy|Crime|Thriller","21","0113161","8012","3.49438202247191",["Hollywood"]],["22","Copycat (1995)","Crime|Drama|Horror|Mystery|Thriller","22","0112722","1710","3.2222222222222223",["serial killer"]],["23","Assassins (1995)","Action|Crime|Thriller","23","0112401","9691","3.125",[]],["24","Powder (1995)","Drama|Sci-Fi","24","0114168","12665","3.125",[]],["25","Leaving Las Vegas (1995)","Drama|Romance","25","0113627","451","3.625",["alcoholism"]],["26","Othello (1995)","Drama","26","0114057","16420","3.5",["Shakespeare"]],["27","Now and Then (1995)","Children|Drama","27","0114011","9263","3.3333333333333335",[]],["28","Persuasion (1995)","Drama|Romance","28","0114117","17015","4.2272727272727275",["In Netflix queue","Jane Austen"]],["29","City of Lost Children, The (Cit\u00e9 des enfants perdus, La) (1995)","Adventure|Drama|Fantasy|Mystery|Sci-Fi","29","0112682","902","4.0131578947368425",["kidnapping"]],["30","Shanghai Triad (Yao a yao yao dao waipo qiao) (1995)","Crime|Drama","30","0115012","37557","3.0",[]],["31","Dangerous Minds (1995)","Drama","31","0112792","9909","3.1842105263157894",["high school","teacher"]],["32","Twelve Monkeys (a.k.a. 12 Monkeys) (1995)","Mystery|Sci-Fi|Thriller","32","0114746","63","3.983050847457627",["time travel","time travel","Brad Pitt","Bruce Willis","mindfuck","Post apocalyptic","post-apocalyptic","remake","time travel","twist ending"]],["34","Babe (1995)","Children|Drama","34","0112431","9598","3.65234375",["Animal movie","pigs","villain nonexistent or not needed for good story"]],["36","Dead Man Walking (1995)","Crime|Drama","36","0112818","687","3.8358208955223883",["death penalty","Nun"]],["38","It Takes Two (1995)","Children|Comedy","38","0113442","33689","2.125",["twins"]],["39","Clueless (1995)","Comedy|Romance","39","0112697","9603","3.293269230769231",["chick flick","funny","Paul Rudd","quotable","seen more than once","Emma","Jane Austen"]],["40","Cry, the Beloved Country (1995)","Drama","40","0112749","34615","4.25",["In Netflix queue","South Africa"]],["41","Richard III (1995)","Drama|War","41","0114279","31174","3.7",["Shakespeare"]],["42","Dead Presidents (1995)","Action|Crime|Drama","42","0112819","11443","3.0",[]],["43","Restoration (1995)","Drama","43","0114272","35196","3.1875",["England"]],["44","Mortal Kombat (1995)","Action|Adventure|Fantasy","44","0113855","9312","2.5434782608695654",[]],["45","To Die For (1995)","Comedy|Drama|Thriller","45","0114681","577","3.3125",["Journalism"]],["46","How to Make an American Quilt (1995)","Drama|Romance","46","0113347","11861","3.066666666666667",["wedding"]],["47","Seven (a.k.a. Se7en) (1995)","Mystery|Thriller","47","0114369","807","3.9753694581280787",["mystery","twist ending","serial killer"]]]
sample_names = ["Toy Story (1995)","Jumanji (1995)","Grumpier Old Men (1995)","Waiting to Exhale (1995)","Father of the Bride Part II (1995)","Heat (1995)","Sabrina (1995)","Tom and Huck (1995)","Sudden Death (1995)","GoldenEye (1995)"]#,"American President, The (1995)","Dracula: Dead and Loving It (1995)","Balto (1995)","Nixon (1995)","Cutthroat Island (1995)","Casino (1995)","Sense and Sensibility (1995)","Four Rooms (1995)","Ace Ventura: When Nature Calls (1995)","Money Train (1995)","Get Shorty (1995)","Copycat (1995)","Assassins (1995)","Powder (1995)","Leaving Las Vegas (1995)","Othello (1995)","Now and Then (1995)","Persuasion (1995)","City of Lost Children, The (Cit\u00e9 des enfants perdus, La) (1995)","Shanghai Triad (Yao a yao yao dao waipo qiao) (1995)","Dangerous Minds (1995)","Twelve Monkeys (a.k.a. 12 Monkeys) (1995)","Babe (1995)","Dead Man Walking (1995)","It Takes Two (1995)","Clueless (1995)","Cry, the Beloved Country (1995)","Richard III (1995)","Dead Presidents (1995)","Restoration (1995)","Mortal Kombat (1995)","To Die For (1995)","How to Make an American Quilt (1995)","Seven (a.k.a. Se7en) (1995)"]

# Endpoint used to give the data with everything needed
@app.route("/whole-table")
def get_whole_table():
    response = jsonify(whole_table)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Endpoint to get the movies names 
@app.route("/whole-names")
def get_whole_names():
    response = jsonify(whole_names)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Other routes for debugging:

@app.route("/movies")
def get_movies():
    response = jsonify(movies)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/links")
def get_links():
    response = jsonify(links)
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

@app.route("/sample-table")
def get_sample_table():
    response = jsonify(sample_table)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/sample-names")
def get_sample_names():
    response = jsonify(sample_names)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response