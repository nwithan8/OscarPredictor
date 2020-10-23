import csv
from urllib.parse import urlencode
from datetime import datetime
import json

import requests
import pandas as pd
from imdbpie import Imdb

TMDB_API_KEY = "df11d86cc7da3a00faaeafc354b858de"

OMDB_API_KEY = "83930f10"

DATA_URL = "https://pkgstore.datahub.io/36661def37f62e4130670ab75e06465a/oscars-nominees-and-winners/data_json/data/d3c23178ad964c76c8ce0ed81762ed7b/data_json.json"

imdb = Imdb()


def get_json(url):
    res = requests.get(url)
    if res:
        return res.json()
    return None


def tmdb_get(endpoint, params: dict = None):
    url = F'https://api.themoviedb.org/3{endpoint}?api_key={TMDB_API_KEY}'
    if params:
        url += f'&{urlencode(params)}'
    return get_json(url=url)


def get_data():
    return get_json(url=DATA_URL)


def get_omdb_movie_data(movie_name):
    data = {'t': movie_name, 'apikey': OMDB_API_KEY}
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


def import_dict_from_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def write_dict_to_json_file(dictionary, filename):
    json_data = json.dumps(dictionary)
    with open(filename, 'w+') as f:
        f.write(json_data)
