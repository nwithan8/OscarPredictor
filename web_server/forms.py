import wtforms
from wtforms.validators import DataRequired, EqualTo, Length

class Movie(wtforms.Form):
    title = wtforms.StringField(
        'Movie Title',
        [DataRequired(message="Please enter a movie title.")]
    )

    runtime = wtforms.IntegerField(
        'Runtime (in minutes)',
        [DataRequired(message="Please enter the movie's runtime in minutes.")]
    )

    budget = wtforms.IntegerField(
        "Budget $",
        [DataRequired(message="Please enter the movie's budget.")]
    )

    revenue = wtforms.IntegerField(
        "Revenue $",
        [DataRequired(message="Please enter the movie's revenue.")]
    )

    rating = wtforms.SelectField(
        'MPAA Rating',
        [DataRequired()],
        choices=[
            ('G', 'G'),
            ('PG', 'PG'),
            ('PG-13', 'PG-13'),
            ('R', 'R')
        ]
    )

    month = wtforms.SelectField(
        'Release Month',
        [DataRequired()],
        choices=[
            ('1', 'January'),
            ('2', 'February'),
            ('3', 'March'),
            ('4', 'April'),
            ('5', 'May'),
            ('6', 'June'),
            ('7', 'July'),
            ('8', 'August'),
            ('9', 'September'),
            ('10', 'October'),
            ('11', 'November'),
            ('12', 'December')
        ]
    )

    box_office = wtforms.IntegerField(
        'Peak Box Office Ranking',
        [DataRequired()]
    )

class Person(wtforms.Form):
    person_name = wtforms.StringField(
        'Name',
        [DataRequired(message="Please enter a name.")]
    )

class Submit(wtforms.Form):
    submit = wtforms.SubmitField('Submit')

class CreateMovie(wtforms.Form):
    movie = wtforms.FormField(Movie)
    director = wtforms.FormField(Person)
    actor1 = wtforms.FormField(Person)
    actor2 = wtforms.FormField(Person)
    actor3 = wtforms.FormField(Person)
    submit = wtforms.SubmitField('Submit')