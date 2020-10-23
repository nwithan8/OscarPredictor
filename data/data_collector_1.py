from imdbpie import Imdb

from data.data_collection import helpers

SINCE_YEAR = 2000
TO_YEAR = 2020

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
    omdb_data = helpers.get_omdb_movie_data(movie_name=movie_name)
    if omdb_data['Response'] == 'False':
        print("Could not get OMDb info.")
        return None
    imdb_id = omdb_data['imdbID']
    imdb_data = helpers.get_imdb_movie_data_by_id(imdb_id=imdb_id)
    if not imdb_data:
        print("Could not get IMDb info.")
        return None
    tmdb_data = helpers.get_tmdb_movie_data_by_imdb_id(imdb_id=imdb_id)
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
    release_date = helpers.get_tmdb_us_release_date(tmdb_id=tmdb_id)
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


imdb = Imdb()
oscar_data = helpers.get_data()
final_entries = []
for item in oscar_data:
    if item['category'] in ['BEST MOTION PICTURE', 'BEST PICTURE', 'OUTSTANDING PICTURE', 'OUTSTANDING PRODUCTION']:
        if SINCE_YEAR <= item['year'] <= TO_YEAR:
            entry = create_movie_entry(movie_name=item['entity'], winner=item['winner'], year=item['year'])
            final_entries.append(entry)
helpers.write_to_csv(entries=final_entries, filename='oscars.csv')
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
