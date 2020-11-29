from data_collection import helpers

directors = {}
oscar_data = helpers.get_data()

SINCE_YEAR = 2000
TO_YEAR = 2020

first_year = None

for item in oscar_data:
    if item['category'] in ['DIRECTING']:
        if not first_year:
            first_year = item['year']
        director_list = helpers.get_director(item['entity'])
        if not director_list:
            print(f"Couldn't get director for {item['entity']}")
        else:
            for director in director_list:
                if director not in directors.keys():  # first appearance
                    directors[director] = {
                        'n': [],
                        'w': []
                    }
                if item['winner'] is True:  # log win
                    directors[director]['w'].append(item['year'])
                else:  # log nom
                    directors[director]['n'].append(item['year'])

director_nom_and_win_tracker = {}
for director_name, wins_and_noms in directors.items():
    director_nom_and_win_tracker[director_name] = {'y': [], 'w': 0, 'n': 0}

years = {}
for year in range(first_year, TO_YEAR+1):
    director_tallies = {}
    for director_name, wins_and_noms in directors.items():
        if year in wins_and_noms['n']:
            director_nom_and_win_tracker[director_name]['n'] += 1
        if year in wins_and_noms['w']:
            director_nom_and_win_tracker[director_name]['y'].append(year)
            director_nom_and_win_tracker[director_name]['w'] += 1
        director_tallies[director_name] = {'y': director_nom_and_win_tracker[director_name]['y'],
                                           'w': director_nom_and_win_tracker[director_name]['w'],
                                           'n': director_nom_and_win_tracker[director_name]['n']
                                           }
    years[f"{year}"] = director_tallies

helpers.write_dict_to_json_file(years, 'smaller_director_totals_by_year.json')