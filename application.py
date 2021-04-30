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
        # SQL direct query TODO
        # shows2 = db.session.execute("""SELECT * FROM shows WHERE title LIKE ?""", {'%' + q + '%'})

        # search format with % wildcards
        srch = "%{}%".format(q)
        shows = Shows.query.filter(Shows.title.like(srch)).all()
        # shows = db.session.query(Shows).filter(Shows.title.like(srch)).all()
        shows = [z.to_json() for z in shows]

    else:
        shows = []

        # for testing 
        # shows = [{"id": 365969, "title": "10-8: Officers on Duty"}, {"id": 1706129, "title": "Officer Ichiro"}, {"id": 1876592, "title": "An Officer and a Movie"}]
    return jsonify(shows)
