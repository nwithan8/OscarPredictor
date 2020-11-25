from flask import Flask, url_for, render_template, redirect, request, flash
from forms import Movie, Person, Submit, CreateMovie

import model.processing as processing


app = Flask(__name__, instance_relative_config=False)
app.config.from_object(__name__)

processing.load_data()

@app.route('/create', methods=['GET'])
def send_form():
    return render_template(
        'create_movies.html',
        form=CreateMovie()
    )

@app.route('/create', methods=['POST'])
def receive_form():
    form = request.form
    flash("Processing results...")
    data = processing.process_form(form=form)
    print(data.csv_format)
    return render_template("wait.html")

if __name__ == "__main__":
    app.run()