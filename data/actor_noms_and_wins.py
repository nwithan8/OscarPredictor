from data_collection import helpers

persons = {}
oscar_data = helpers.get_data()

SINCE_YEAR = 2000
TO_YEAR = 2020

first_year = None

for item in oscar_data:
    if item['category'] in ['ACTOR', "ACTOR IN A LEADING ROLE"]:
        if not first_year:
            first_year = item['year']
        name = item['entity']
        if name not in persons.keys():  # first appearance
            persons[name] = {
                'noms': [],
                'wins': []
            }
        if item['winner'] is True:  # log win
            persons[name]['wins'].append(item['year'])
        else:  # log nom
            persons[name]['noms'].append(item['year'])

nom_and_win_tracker = {}
for name, wins_and_noms in persons.items():
    nom_and_win_tracker[name] = {'win_years': [], 'wins': 0, 'noms': 0}

years = {}
for year in range(first_year, TO_YEAR + 1):
    tallies = {}
    for name, wins_and_noms in persons.items():
        if year in wins_and_noms['noms']:
            nom_and_win_tracker[name]['noms'] += 1
        if year in wins_and_noms['wins']:
            nom_and_win_tracker[name]['win_years'].append(year)
            nom_and_win_tracker[name]['wins'] += 1
        tallies[name] = {'win_years': nom_and_win_tracker[name]['win_years'],
                         'wins': nom_and_win_tracker[name]['wins'],
                         'noms': nom_and_win_tracker[name]['noms']
                         }
    years[f"{year}"] = tallies

helpers.write_dict_to_json_file(years, 'actors_totals_by_year.json')
"""
for year in years:
    print(f"{year['year']}:")
    for director_name, wins_and_noms in year['directors'].items():
        print(f"-- {director_name}:\tWins: {wins_and_noms['wins']}\tNoms: {wins_and_noms['noms']}")
"""