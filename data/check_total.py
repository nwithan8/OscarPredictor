import json
import argparse
from data_collection import helpers

FILES = {
    'director': 'director_totals_by_year.json',
    'actor': 'actors_totals_by_year.json',
    'actress': 'actress_totals_by_year.json'
}

parser = argparse.ArgumentParser()
parser.add_argument('type', help='director, actor or actress')
args = parser.parse_args()

data = helpers.import_dict_from_json_file(FILES[args.type])

while True:
    name = input(f"{args.type} name: ")
    year = input(f"year: ")
    results = data[year].get(name)
    if results:
        if int(year) in results['win_years']:
            print(f"Won this year. Noms: {results['noms']}, Wins: {results['wins']}")
        else:
            print(f"Noms: {results['noms']}, Wins: {results['wins']}")
    else:
        print(f"Could not find {args.type}, so -> Noms: 0, Wins: 0")

