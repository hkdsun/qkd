from flask import Flask, request, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy
import os, json
from twilio.rest import TwilioRestClient


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
client = TwilioRestClient()

from models import Entry, EntrySchema

entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)

@app.route('/entries', methods=['GET', 'POST'])
def entries():
    entries = []
    errors = []

    if request.method == "POST":
        json_data = request.get_json()
        entry, errors = entry_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        try:
            db.session.add(entry)
            db.session.commit()
        except:
            errors.append("Unable to add item to database.")
            return jsonify({"error": errors}), 422
        entries.append(entry)
    if request.method == "GET":
        entries += db.session.query(Entry).all()

    result = entries_schema.dump(entries)
    return jsonify({'entries': result.data})


@app.route('/', methods=['GET'])
def index():
    return make_response(open('templates/index.html').read())


if __name__ == '__main__':
    app.run()
