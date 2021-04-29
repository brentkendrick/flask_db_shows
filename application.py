# Searches for shows using Ajax with JSON

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

# To run the app: on the command line, first:  export FLASK_APP=application

# To test SQLAlchemy commands in the CLI, run python and run "from application import Shows"



app = Flask(__name__)


ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shows.db"
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ""

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Connect to database
db = SQLAlchemy(app)

# Name the class after the table name or use dunder to name the table
class Shows(db.Model):
    __tablename__='shows'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)

    def __repr__(self):
        lst = f'{{"id":{self.id}, "title":"{self.title}"}}'

        return lst

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    q = request.args.get("q")
    if q:
        # shows = db.execute("SELECT * FROM shows WHERE title LIKE ?", "%" + q + "%")
        srch = "%{}%".format(q)
        shows = Shows.query.filter(Shows.title.like(srch)).all()
        shows = [show.__repr__() for show in shows]
    else:
        shows = []
    return shows
