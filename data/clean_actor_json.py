from data_collection import helpers

persons = {}
oscar_data = helpers.get_data()

SINCE_YEAR = 2000
TO_YEAR = 2020

first_year = None

for item in oscar_data:
    if item['category'] in ['ACTOR', "ACTOR IN A LEADING ROLE", 'ACTRESS', "ACTRESS IN A LEADING ROLE"]:
        if not first_year:
            first_year = item['year']
        name = item['entity']
        if name not in persons.keys():  # first appearance
            persons[name] = {
                'n': [],
                'w': []
            }
        if item['winner'] is True:  # log win
            persons[name]['w'].append(item['year'])
        else:  # log nom
            persons[name]['n'].append(item['year'])

nom_and_win_tracker = {}
for name, wins_and_noms in persons.items():
    nom_and_win_tracker[name] = {'y': [], 'w': 0, 'n': 0}

years = {}
for year in range(first_year, TO_YEAR + 1):
    tallies = {}
    for name, wins_and_noms in persons.items():
        if year in wins_and_noms['n']:
            nom_and_win_tracker[name]['n'] += 1
        if year in wins_and_noms['w']:
            nom_and_win_tracker[name]['y'].append(year)
            nom_and_win_tracker[name]['w'] += 1
        tallies[name] = {'y': nom_and_win_tracker[name]['y'],
                         'w': nom_and_win_tracker[name]['w'],
                         'n': nom_and_win_tracker[name]['n']
                         }
    years[f"{year}"] = tallies

helpers.write_dict_to_json_file(years, 'smaller_actors_totals_by_year.json')