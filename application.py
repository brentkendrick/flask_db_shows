# Searches for shows using Ajax with JSON

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

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

    def to_json(self):
        return {
            "id":self.id,
            "title":self.title
        }

    # def __repr__(self):
    #     lst = f'"title":"{self.title}"'

    #     return lst

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    q = request.args.get("q")
    # q = "Officer"
    if q:
        # shows2 = db.session.execute("""SELECT * FROM shows WHERE title LIKE ?""", {'%' + q + '%'})
        # sqlitis translation: select([shows]).where(text('title'))
        srch = "%{}%".format(q)
        shows2 = Shows.query.filter(Shows.title.like(srch)).all()
        # shows2 = db.session.query(Shows).filter(Shows.title.like(srch)).all()
        shows2 = [z.to_json() for z in shows2]

    else:
        shows2 = []

        # for testing 
        # shows2 = [{"id": 365969, "title": "10-8: Officers on Duty"}, {"id": 1706129, "title": "Officer Ichiro"}, {"id": 1876592, "title": "An Officer and a Movie"}, {"id": 3001516, "title": "Ridin' Dirty with Officer Turner"}, {"id": 3457306, "title": "Bonnie Blake: Parole Officer"}, {"id": 5171576, "title": "Officer Hardbody"}, {"id": 6823170, "title": "Officer Bob"}, {"id": 7575588, "title": "NUTV Officer Election Coverage"}, {"id": 8362676, "title": "Officer Hansel, Burbank PD"}, {"id": 10348734, "title": "Police Code Zero: Officer Under Attack"}, {"id": 10380660, "title": "Young Army Officer"}, {"id": 12295806, "title": "Officer Eric Hale"}, {"id": 12409398, "title": "Officer Down the Next 24 Hours"}, {"id": 13016298, "title": "The Officer Tatum"}]
    return jsonify(shows2)
