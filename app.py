from flask import Flask, request, jsonify, make_response, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os
from twilio.rest import TwilioRestClient
from twilio import twiml
from pytz import timezone


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
        print json_data
        entry, errors = entry_schema.load(json_data)
        utc_time = entry.date
        utc_time = utc_time.replace(tzinfo=timezone("UTC"))
        entry.date = utc_time.astimezone(timezone("US/Eastern"))
        if errors:
            return jsonify(errors), 422
        try:
            db.session.add(entry)
            db.session.commit()
            result = entry_schema.dump(entry)
            return jsonify({'entry': result.data})
        except:
            return jsonify({"error": errors}), 422
    if request.method == "GET":
        entries += db.session.query(Entry).all()
        result = entries_schema.dump(entries)
        return jsonify({'entries': result.data})


@app.route('/sms', methods=['POST'])
def receive_sms():
    if request.method == "POST":
        from_number = request.values.get('From', None)
        body = request.values.get('Body', None)
        if from_number and body:
            entry = Entry(body=body)
            try:
                db.session.add(entry)
                db.session.commit()
            except:
                message = "I'm sorry I couldn't get that through. Maybe you can try again"
            message = "Noted, sir!"
        else:
            return make_response("invalid request")
    else:
        return make_response("invalid request"), 422
    resp = twiml.Response()
    resp.message(message)
    return make_response(str(resp))


@app.route('/', methods=['GET'])
def index():
    return make_response(open('templates/index.html').read())


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
