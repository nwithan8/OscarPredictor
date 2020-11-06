import json
import argparse
from data_collection import helpers

FILES = {
    'director': ['director_totals_by_year.json'],
    'actor': ['actors_totals_by_year.json', 'actress_totals_by_year.json'],
    'actress': ['actors_totals_by_year.json', 'actress_totals_by_year.json']
}

parser = argparse.ArgumentParser()
parser.add_argument('type', help='director, actor or actress')
args = parser.parse_args()

data = []
for file in FILES[args.type]:
    data.append(helpers.import_dict_from_json_file(file))

while True:
    name = input(f"{args.type} name: ")
    year = input(f"year: ")
    for dataset in data:
        results = dataset[year].get(name)
        if results:
            if int(year) in results['win_years']:
                print(f"Won this year. Noms: {results['noms']}, Wins: {results['wins']}")
            else:
                print(f"Noms: {results['noms']}, Wins: {results['wins']}")
            break
        else:
            print(f"Could not find {args.type}, so -> Noms: 0, Wins: 0")

