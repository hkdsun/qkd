from app import db
from datetime import datetime
from marshmallow import Schema, fields, post_load
from pytz import timezone

eastern = timezone('US/Eastern')
utc = timezone('UTC')


class EntrySchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.DateTime()
    body = fields.String()

    @post_load
    def make_entry(self, data):
        return Entry(**data)


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime())
    user = db.Column(db.String())
    body = db.Column(db.String())

    def __init__(self, body, date=None, id=None):
        if not date:
            date = utc.normalize(datetime.now(tz=eastern))
        self.id = id
        self.date = date
        self.body = body

    def __repr__(self):
        return '<id {}>'.format(self.id)
