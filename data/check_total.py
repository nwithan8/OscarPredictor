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
parser.add_argument('--simple', action="store_true", help="Simplified output")
args = parser.parse_args()

data = []
for file in FILES[args.type]:
    data.append(helpers.import_dict_from_json_file(file))

while True:
    name = input(f"{args.type} name: ")
    year = input(f"year: ")
    dataset_number = 1
    for dataset in data:
        results = dataset[year].get(name)
        if results:
            if int(year) in results['win_years']:
                if args.simple:
                    print(f"TRUE\t{results['noms']}\t{results['wins']}")
                else:
                    print(f"Won this year. Noms: {results['noms']}, Wins: {results['wins']}")
            else:
                if args.simple:
                    print(f"FALSE\t{results['noms']}\t{results['wins']}")
                else:
                    print(f"Noms: {results['noms']}, Wins: {results['wins']}")
            break
        else:
            if dataset_number >= len(data):
                if args.simple:
                    print(f"FALSE\t0\t0")
                else:
                    print(f"Could not find {args.type}, so -> Noms: 0, Wins: 0")
            dataset_number += 1

