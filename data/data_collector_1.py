import csv
from urllib.parse import urlencode
from datetime import datetime

import requests
import pandas as pd
from imdbpie import Imdb

SINCE_YEAR = 2000
TO_YEAR = 2020


TMDB_API_KEY = "df11d86cc7da3a00faaeafc354b858de"


def get_json(url):
    res = requests.get(url)
    if res:
        return res.json()
    return None


def tmdb_get(endpoint, params: dict = None):
    url = 'https://api.themoviedb.org/3' + endpoint + "?api_key=" + TMDB_API_KEY
    if params:
        url += '&' + urlencode(params)
    return get_json(url=url)


def get_data():
    return get_json(
        url="https://pkgstore.datahub.io/36661def37f62e4130670ab75e06465a/oscars-nominees-and-winners/data_json/data/d3c23178ad964c76c8ce0ed81762ed7b/data_json.json")


def get_omdb_movie_data(movie_name):
    data = {'t': movie_name, 'apikey': '83930f10'}
    url = f"http://www.omdbapi.com/?{urlencode(data)}"
    return get_json(url=url)


def get_imdb_movie_data_by_name(movie_name):
    results = imdb.search_for_title(movie_name)
    if results:
        return get_imdb_movie_data_by_id(imdb_id=results[0]['imdb_id'])


def get_imdb_movie_data_by_id(imdb_id):
    return imdb.get_title(imdb_id=imdb_id)


def get_tmdb_movie_data_by_imdb_id(imdb_id):
    search_results = tmdb_get(endpoint=f'/find/{imdb_id}', params={'external_source': 'imdb_id'})
    if search_results:
        # print(search_results)
        tmdb_id = search_results['movie_results'][0]['id']
        return tmdb_get(endpoint=f'/movie/{tmdb_id}')
    return None


def get_director(movie_name):
    json_data = get_omdb_movie_data(movie_name)
    if json_data and json_data.get('Director'):
        return json_data['Director'].split(", ")
    return None


def parse_release_date(tmdb_release_date):
    split = tmdb_release_date.split('-')
    return split


def convert_date_to_string(tmdb_release_date):
    date = datetime.strptime(tmdb_release_date, '%Y-%m-%dT%H:%M:%S.000Z')
    return date.strftime("%Y-%m-%d")


def get_tmdb_us_release_date(tmdb_id):
    data = tmdb_get(endpoint=f'/movie/{tmdb_id}/release_dates')
    if data:
        for release in data['results']:
            if release['iso_3166_1'] == 'US':
                for date in release['release_dates']:
                    if date['type'] == 3:
                        return parse_release_date(convert_date_to_string(date['release_date']))
    return None


"""
def actor_in_movie(actor_name, movie_name):
    json_data = get_movie_data(movie_name)
    if json_data and json_data.get('Actors'):
        actors = json_data['Actors'].split(", ")
        if actor_name in actors:
            return True
    return False


def director_of_movie(director_name, movie_name):
    json_data = get_movie_data(movie_name)
    if json_data and json_data.get('Director'):
        movie_director_list = json_data['Director'].split(", ")
        if director_name in movie_director_list:
            return True
    return False
"""


def create_movie_entry(movie_name, winner: bool, year):
    movie_dict = {}
    print(f"Building entry for '{movie_name}'...")
    omdb_data = get_omdb_movie_data(movie_name=movie_name)
    if omdb_data['Response'] == 'False':
        print("Could not get OMDb info.")
        return None
    imdb_id = omdb_data['imdbID']
    imdb_data = get_imdb_movie_data_by_id(imdb_id=imdb_id)
    if not imdb_data:
        print("Could not get IMDb info.")
        return None
    tmdb_data = get_tmdb_movie_data_by_imdb_id(imdb_id=imdb_id)
    if not tmdb_data:
        print("Could not get TMDb info.")
        return None
    tmdb_id = tmdb_data['id']
    movie_dict['title'] = omdb_data.get('Title')
    movie_dict['won'] = winner
    movie_dict['ceremonyYear'] = year
    movie_dict['runningTime'] = imdb_data['base'].get('runningTimeInMinutes')
    movie_dict['budget'] = tmdb_data['budget']
    movie_dict['revenue'] = tmdb_data['revenue']
    movie_dict['gross'] = tmdb_data['revenue'] - tmdb_data['budget']
    movie_dict['directorName'] = omdb_data['Director']
    movie_dict['MPAARating'] = omdb_data['Rated']
    for metric in omdb_data['Ratings']:
        if metric['Source'] == 'Rotten Tomatoes':
            movie_dict['rottenTomatoesScore'] = int(metric['Value'].replace('%', ''))
    release_date = get_tmdb_us_release_date(tmdb_id=tmdb_id)
    if not release_date:
        print("Could not get release date. Flagging release date.")
        movie_dict['USReleaseMonth'] = "MISSING"
        movie_dict['USReleaseYear'] = "MISSING"
    else:
        if year > int(release_date[0]):
            print("Wrong movie, likely a remake and grabbed the old version by mistake. Removing entire entry.")
            return None
        elif year < int(release_date[0]) and int(release_date[1]) > 1:
            print("Movie that came out past January but was still in the awards ceremony? Flagging release date.")
            movie_dict['USReleaseMonth'] = "MISSING"
            movie_dict['USReleaseYear'] = "MISSING"
        else:
            movie_dict['USReleaseMonth'] = int(release_date[1])
            movie_dict['USReleaseYear'] = int(release_date[0])
    # print(movie_dict)
    return movie_dict


def write_to_csv(entries, filename):
    csv_columns = []
    for key in entries[0].keys():
        csv_columns.append(key)
    with open(filename, 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for entry in entries:
            if entry:
                print(f"Saving {entry['title']} entry...")
                writer.writerow(entry)


imdb = Imdb()
oscar_data = get_data()
final_entries = []
for item in oscar_data:
    if item['category'] in ['BEST MOTION PICTURE', 'BEST PICTURE', 'OUTSTANDING PICTURE', 'OUTSTANDING PRODUCTION']:
        if SINCE_YEAR <= item['year'] <= TO_YEAR:
            entry = create_movie_entry(movie_name=item['entity'], winner=item['winner'], year=item['year'])
            final_entries.append(entry)
write_to_csv(entries=final_entries, filename='oscars.csv')
"""
actors = {}
actresses = {}
directors = {}
movies = {}
for item in oscar_data:
    if item['category'] in ['ACTOR', "ACTOR IN A LEADING ROLE"]:
        if item['entity'] not in actors.keys():  # first appearance
            actors[item['entity']] = {
                'wins': [],
                'total_noms': 0,
                'total_wins': 0
            }
        if item['winner'] is True:  # log win
            actors[item['entity']]['wins'].append(
                {
                    'year': item['year'],
                    'prior_nom_count': actors[item['entity']]['total_noms'],
                    'prior_win_count': actors[item['entity']]['total_wins']
                }
            )
            actors[item['entity']]['total_noms'] += 1
            actors[item['entity']]['total_wins'] += 1
        else:  # log nom
            actors[item['entity']]['total_noms'] += 1
    elif item['category'] in ['ACTRESS', "ACTRESS IN A LEADING ROLE"]:
        if item['entity'] not in actresses.keys():  # first appearance
            actresses[item['entity']] = {
                'wins': [],
                'total_noms': 0,
                'total_wins': 0
            }
        if item['winner'] is True:  # log win
            actresses[item['entity']]['wins'].append(
                {
                    'year': item['year'],
                    'prior_nom_count': actresses[item['entity']]['total_noms'],
                    'prior_win_count': actresses[item['entity']]['total_wins']
                }
            )
            actresses[item['entity']]['total_noms'] += 1
            actresses[item['entity']]['total_wins'] += 1
        else:  # log nom
            actresses[item['entity']]['total_noms'] += 1
    elif item['category'] in ['DIRECTING']:
        movies[item['year']] = item['entity']
        director_list = get_director(item['entity'])
        if not director_list:
            print(f"Couldn't get director for {item['entity']}")
        else:
            for director in director_list:
                if director not in directors.keys():  # first appearance
                    directors[director] = {
                        'wins': [],
                        'total_noms': 0,
                        'total_wins': 0
                    }
                if item['winner'] is True:  # log win
                    directors[director]['wins'].append(
                        {
                            'year': item['year'],
                            'prior_nom_count': directors[director]['total_noms'],
                            'prior_win_count': directors[director]['total_wins']
                        }
                    )
                    directors[director]['total_noms'] += 1
                    directors[director]['total_wins'] += 1
                else:  # log nom
                    directors[director]['total_noms'] += 1

actors_by_year = {}
actresses_by_year = {}
directors_by_year = {}

for name, v in actors.items():
    for win in v['wins']:
        if movies.get(win['year']):
            in_best_picture = actor_in_movie(actor_name=name, movie_name=movies[win['year']])
        else:
            in_best_picture = False
        actors_by_year[win['year']] = {
            'name': name,
            'prior_noms': win['prior_nom_count'],
            'prior_wins': win['prior_win_count'],
            'in_best_picture': in_best_picture
        }
with open('actors.csv', 'w+') as f:
    f.write("year,name,prior_noms,prior_wins,in_best_pic\n")
    for year, v in actors_by_year.items():
        f.write(f"{year},{v['name']},{v['prior_noms']},{v['prior_wins']},{v['in_best_picture']}\n")

for name, v in actresses.items():
    for win in v['wins']:
        if movies.get(win['year']):
            in_best_picture = actor_in_movie(actor_name=name, movie_name=movies[win['year']])
        else:
            in_best_picture = False
        actresses_by_year[win['year']] = {
            'name': name,
            'prior_noms': win['prior_nom_count'],
            'prior_wins': win['prior_win_count'],
            'in_best_picture': in_best_picture
        }
with open('actresses.csv', 'w+') as f:
    f.write("year,name,prior_noms,prior_wins,in_best_pic\n")
    for year, v in actresses_by_year.items():
        f.write(f"{year},{v['name']},{v['prior_noms']},{v['prior_wins']},{v['in_best_picture']}\n")

for name, v in directors.items():
    for win in v['wins']:
        if movies.get(win['year']):
            in_best_picture = director_of_movie(director_name=name, movie_name=movies[win['year']])
        else:
            in_best_picture = False
        directors_by_year[win['year']] = {
            'name': name,
            'prior_noms': win['prior_nom_count'],
            'prior_wins': win['prior_win_count'],
            'in_best_picture': in_best_picture
        }
with open('directors.csv', 'w+') as f:
    f.write("year,name,prior_noms,prior_wins,in_best_pic\n")
    for year, v in directors_by_year.items():
        f.write(f"{year},{v['name']},{v['prior_noms']},{v['prior_wins']},{v['in_best_picture']}\n")
"""
