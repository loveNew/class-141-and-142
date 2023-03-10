import csv

all_movies = []

with open("final.csv",encoding="utf8") as f:
    data1 = csv.reader(f)
    data = list(data1)
    all_movies = data[1:]

liked_movies = []
disliked_movies= []
did_not_watch = []