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
                        'noms': [],
                        'wins': []
                    }
                if item['winner'] is True:  # log win
                    directors[director]['wins'].append(item['year'])
                else:  # log nom
                    directors[director]['noms'].append(item['year'])

director_nom_and_win_tracker = {}
for director_name, wins_and_noms in directors.items():
    director_nom_and_win_tracker[director_name] = {'win_years': [], 'wins': 0, 'noms': 0}

years = {}
for year in range(first_year, TO_YEAR+1):
    director_tallies = {}
    for director_name, wins_and_noms in directors.items():
        if year in wins_and_noms['noms']:
            director_nom_and_win_tracker[director_name]['noms'] += 1
        if year in wins_and_noms['wins']:
            director_nom_and_win_tracker[director_name]['win_years'].append(year)
            director_nom_and_win_tracker[director_name]['wins'] += 1
        director_tallies[director_name] = {'win_years': director_nom_and_win_tracker[director_name]['win_years'],
                                           'wins': director_nom_and_win_tracker[director_name]['wins'],
                                           'noms': director_nom_and_win_tracker[director_name]['noms']
                                           }
    years[f"{year}"] = director_tallies

helpers.write_dict_to_json_file(years, 'director_totals_by_year.json')
"""
for year in years:
    print(f"{year['year']}:")
    for director_name, wins_and_noms in year['directors'].items():
        print(f"-- {director_name}:\tWins: {wins_and_noms['wins']}\tNoms: {wins_and_noms['noms']}")
"""