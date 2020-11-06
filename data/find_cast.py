import json
import argparse
from data_collection import helpers

import imdb

im = imdb.IMDb()

parser = argparse.ArgumentParser()
parser.add_argument('count', type=int, help='number of actors to list')
args = parser.parse_args()

while True:
    movieId = None
    name = input(f"Movie title: ")
    year = input(f"Movie year: ")
    if int(year) > 2020:
        print("Typo in year")
        pass
    else:
        results = im.search_movie(name)
        if results:
            for this_movie in results:
                if (int(year) - 1) < this_movie.data['year'] < (int(year) + 1):
                    print(f"Using {this_movie.data['title']} ({this_movie.data['year']})...")
                    movieId = this_movie.movieID
                    break
            movie = im.get_movie(movieId)
            for person in movie['cast'][0:args.count]:
                print(person.data['name'])
        else:
            print("Could not find movie.")
