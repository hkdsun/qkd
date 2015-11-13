from app import db
from datetime import datetime
from marshmallow import Schema, fields, post_load
from pytz import timezone


eastern = timezone('US/Eastern')
utc = timezone('UTC')


class BaseSchema(Schema):
    __model__ = None

    @post_load
    def make_model(self, data):
        return self.__model__(**data)


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    username = db.Column(db.String(), db.ForeignKey('users.username'))
    body = db.Column(db.String())

    def __init__(self, body, date=None, id=None):
        if not date:
            date = datetime.utcnow()
        self.id = id
        self.date = date
        self.body = body

    def __repr__(self):
        return '<id {}>'.format(self.id)


class EntrySchema(BaseSchema):
    __model__ = Entry
    id = fields.Int(dump_only=True)
    date = fields.LocalDateTime()
    body = fields.String()


class User(db.Model):
    __tablename__ = "users"
    username = db.Column('username', db.String(20), primary_key=True, unique=True, index=True)
    password = db.Column('password', db.String(16))
    email = db.Column('email', db.String(50), unique=True, index=True)
    first_name = db.Column('first_name', db.String())
    last_name = db.Column('last_name', db.String())
    registered_on = db.Column('registered_on', db.DateTime)
    entries = db.relationship("Entry", backref="user")

    def __init__(self, username, password, email, first_name, last_name):
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.username)

    def __repr__(self):
        return '<User %r>' % (self.username)


class UserSchema(BaseSchema):
    __model__ = User
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    registered_on = fields.DateTime()
