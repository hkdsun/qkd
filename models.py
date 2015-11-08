from app import db
from datetime import date
from marshmallow import Schema, fields, pprint, post_load


class EntrySchema(Schema):
    id = fields.Int(dump_only=True)
    url = fields.URL()
    body = fields.String()

    @post_load
    def make_entry(self, data):
        return Entry(**data)


class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    user = db.Column(db.String())
    body = db.Column(db.String())

    def __init__(self, url, body):
        self.url = url
        self.body = body

    def __repr__(self):
        return '<id {}>'.format(self.id)
