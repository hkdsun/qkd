from flask import Flask, request, jsonify, make_response, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os
from twilio.rest import TwilioRestClient
from twilio import twiml
from pytz import timezone
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
twilio = TwilioRestClient()

from models import Entry, EntrySchema

entry_schema = EntrySchema()
entries_schema = EntrySchema(many=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    return User.query.get(str(username))


@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return make_response(open('templates/sign-up.html').read())
    if request.method == 'POST':
        user = User(request.form['username'] , request.form['password'],request.form['email'])
        db.session.add(user)
        db.session.commit()
        flash('User successfully registered')
        return redirect(url_for('login'))


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return make_response(open('templates/sign-in.html').read())
    return redirect(url_for('index'))


@app.route('/entries/<int:entry_id>', methods=['GET', 'POST', 'DELETE'])
def get_entry(entry_id):
    errors = []
    entry = None
    # Getting an entry
    if request.method == "GET":
        try:
            entry = db.session.query(Entry).get(entry_id)
        except:
            errors.append("Entry not found")
        if entry:
            result = entry_schema.dump(entry)
            return jsonify(result.data)
        else:
            errors.append("Entry not found")
            return jsonify({"error": errors}), 422
    # Updating an entry #
    if request.method == "POST":
        print "Got post", request.data
        try:
            entry = db.session.query(Entry).get(entry_id)
            json_data = request.get_json()
            new_entry, errors = entry_schema.load(json_data)

            utc_time = new_entry.date
            utc_time = utc_time.replace(tzinfo=timezone("UTC"))
            new_entry.date = utc_time.astimezone(timezone("US/Eastern"))

            entry.body = new_entry.body
            db.session.commit()
        except:
            errors.append("Couldn't get the entry from the DB")
        if entry:
            result = entry_schema.dump(entry)
            print result.data
            return jsonify(result.data)
        else:
            errors.append("Couldn't find entry you're looking for")
            return jsonify({"error": errors}), 422
    if request.method == "DELETE":
        entry = Entry.query.get(entry_id)
        if entry:
            try:
                db.session.delete(entry)
                db.session.commit()
                result = entry_schema.dump(entry)
                return jsonify(result.data)
            except:
                raise
                return jsonify({"error": errors}), 422



@app.route('/entries', methods=['GET', 'POST'])
def entries():
    entries = []
    errors = []

    if request.method == "POST":
        json_data = request.get_json()
        if 'id' in json_data:
            return get_entry(json_data['id'])
        entry, errors = entry_schema.load(json_data)
        if errors:
            return jsonify(errors), 422
        try:
            db.session.add(entry)
            db.session.commit()
            result = entry_schema.dump(entry)
            return jsonify(result.data)
        except:
            raise
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
