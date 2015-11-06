from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os
from twilio.rest import TwilioRestClient


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
client = TwilioRestClient()

from models import Entry


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    entries = []
    if request.method == "POST":
        # get url that the user has entered
        body = request.form['body']
        entry = Entry(
            url="",
            body=body
        )
        try:
            db.session.add(entry)
            db.session.commit()
            entries = db.session.query(Entry).order_by(Entry.id)[-10:]
        except:
            errors.append("Unable to add item to database")
    if request.method == "GET":
        entries = db.session.query(Entry).order_by(Entry.id)[-10:]
    return render_template('index.html', errors=errors, entries=entries)

if __name__ == '__main__':
    app.run()
