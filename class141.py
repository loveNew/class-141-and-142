from flask import Flask,jsonify,request
from storage import all_movies, liked_movies, did_not_watch, disliked_movies
from demographic_filtering import output
from content_based_filtering import get_recommendations
import csv 

all_movies = []

with open("movies.csv")as f:
    data1 = csv.reader(f)
    data = list(data1)
    all_movies = data[1:]

liked_movies = []
disliked_movies = []
did_not_watch = []

app = Flask(__name__)

@app.route("/get_movie")
def get_movie():
    movie_data = {
        "title": all_movies[0][19],
        'poster_link': all_movies[0][27], 
        'release_date': all_movies[0][13] or "N/A", 
        'duration': all_movies[0][15], 
        'rating': all_movies[0][20], 
        'overview': all_movies[0][9]
    }
    return jsonify({
        "data": movie_data,
        "status":"success"
    })

@app.route("/liked_movies")
def liked_movies():
    global all_movies
    movie = all_movies[0]
    liked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
       "status":"success" 
    }),201

@app.route("/disliked_movies")
def disliked_movies():
    global all_movies
    movie = all_movies[0]
    disliked_movies.append(movie)
    all_movies.pop(0)
    return jsonify({
       "status":"success" 
    }),201

@app.route("/did_not_watch")
def did_not_watch():
    global all_movies
    movie = all_movies[0]
    did_not_watch.append(movie)
    all_movies.pop(0)
    return jsonify({
       "status":"success" 
    }),201

@app.route("/popular-movies")
def popularMovies():
    movie_data = []
    for i in output:
        data = {
            "title": i[0],
            'poster_link': i[1], 
            'release_date': i[2] or "N/A", 
            'duration': i[3], 
            'rating': i[4], 
            'overview': i[5]
        }
        movie_data.append(data)
    return jsonify({
        "data": movie_data,
        "status":"success"
    }),200

@app.route("/recommended-movies")
def recommendedMovies():
    all_recommended = []
    for i in liked_movies:
        reco_output = get_recommendations(i[19])
        for j in reco_output:
            all_recommended.append(j)
    import itertools
    all_recommended.sort()
    all_recommended = list(i for i,_ in itertools.groupby(i))
    movie_data = []
    for i in all_recommended:
        data = {
            "title": i[0],
            'poster_link': i[1], 
            'release_date': i[2] or "N/A", 
            'duration': i[3], 
            'rating': i[4], 
            'overview': i[5]
        }
        movie_data.append(data)
    return jsonify({
        "data": movie_data,
        "status":"success"
    }),200

if __name__ == "__main__":
    app.run()