import model.helpers as helpers

_form_to_var = {
    'movie-title': 'title',
    'movie-runtime': 'runningTime',
    'movie-budget': 'budget',
    'movie-revenue': 'revenue',
    'movie-box_office': 'peakBoxOfficeRanking',
    'movie-month': 'USReleaseMonth',
    'movie-rating': 'MPAARating',
    'director-person_name': 'directorName',
    'actor1-person_name': 'actor1Name',
    'actor2-person_name': 'actor2Name',
    'actor3-person_name': 'actor3Name'
}

class FormData:
    def __init__(self, form: dict):
        self._parse_form_data(data=form)
        self._complete_movie_data()
        self._complete_people_data()

    def _parse_form_data(self, data: dict):
        for item in data:
            if item != 'submit':
                setattr(self, _form_to_var[item], data[item])

    def _complete_movie_data(self):
        try:
            self.budget = int(self.budget)
        except:
            self.budget = 0
        try:
            self.revenue = int(self.revenue)
        except:
            self.revenue = 0
        self.gross = self.revenue - self.budget
        self.ceremonyYear = 2020
        self.USReleaseYear = self.ceremonyYear - 1
        if int(self.USReleaseMonth) in [1, 2]:
            self.USReleaseYear = self.ceremonyYear
        self.rottenTomatoesScore = 80

    def _complete_people_data(self):
        self.director = look_up_person(person_type='director',
                                  name=self.directorName,
                                  year=self.ceremonyYear)
        for actor_number in range(1, 4):
            actor = look_up_person(name=vars(self)[f'actor{actor_number}Name'],
                                   person_type='actor',
                                   year=self.ceremonyYear)
            setattr(self, f"actor{actor_number}", actor)

    @property
    def csv_format(self):
        return f"{self.title},FALSE,{self.ceremonyYear},{self.runningTime},{self.budget},{self.revenue},{self.gross},{self.director.name},{self.director.won},{self.director.nominations},{self.director.wins},{self.actor1.name},{self.actor1.won},{self.actor1.nominations},{self.actor1.wins},{self.actor2.name},{self.actor2.won},{self.actor2.nominations},{self.actor2.wins},{self.actor3.name},{self.actor3.won},{self.actor3.nominations},{self.actor3.wins},{self.MPAARating},{self.rottenTomatoesScore},{self.USReleaseMonth},{self.USReleaseYear},{self.peakBoxOfficeRanking}"


def process_form(form: dict):
    return FormData(form=form)


DIRECTOR_DATA = []
ACTOR_DATA = []

PERSON_DATA_FILES = {
    'director': ['model\\director_totals_by_year.json'],
    'actor': ['model\\actors_totals_by_year.json', 'model\\actress_totals_by_year.json'],
    'actress': ['model\\actors_totals_by_year.json', 'model\\actress_totals_by_year.json']
}

def _load_person_data(person_type: str):
    data = []
    for file in PERSON_DATA_FILES[person_type]:
        data.append(helpers.import_dict_from_json_file(file))
    return data

def _load_director_data():
    global DIRECTOR_DATA
    DIRECTOR_DATA = _load_person_data('director')

def _load_actor_data():
    global ACTOR_DATA
    ACTOR_DATA = _load_person_data('actor')

def load_data():
    _load_director_data()
    _load_actor_data()

class Person:
    def __init__(self, name: str, awards: dict, won: bool = False):
        self.name = name
        self.nominations = awards.get('noms', 0)
        self.wins = awards.get('wins', 0)
        self.won = won

def look_up_person(name: str, person_type: str, year: int = 2020):
    if person_type == 'director':
        if not DIRECTOR_DATA:
            _load_director_data()
        dataset_number = 1
        for dataset in DIRECTOR_DATA:
            results = dataset[str(year)].get(name)
            if results:
                return Person(name=name, awards=results, won=True if int(year) in results['win_years'] else False)
            else:
                if dataset_number >= len(DIRECTOR_DATA):
                    return Person(name=name, awards={})
                dataset_number += 1
    elif person_type == 'actor':
        if not ACTOR_DATA:
            _load_actor_data()
        dataset_number = 1
        for dataset in ACTOR_DATA:
            results = dataset[str(year)].get(name)
            if results:
                return Person(name=name, awards=results, won=True if int(year) in results['win_years'] else False)
            else:
                if dataset_number >= len(ACTOR_DATA):
                    return Person(name=name, awards={})
                dataset_number += 1
