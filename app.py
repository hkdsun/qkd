from flask import Flask, request, jsonify, make_response, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os, json
from twilio.rest import TwilioRestClient


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
twilio = TwilioRestClient()

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
            result = entry_schema.dump(entry)
            return jsonify({'entry': result.data})
        except:
            errors.append("Unable to add item to database.")
            return jsonify({"error": errors}), 422
    if request.method == "GET":
        entries += db.session.query(Entry).all()
        result = entries_schema.dump(entries)
        return jsonify({'entries': result.data})


@app.route('/', methods=['GET'])
def index():
    return make_response(open('templates/index.html').read())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
