from google.appengine.ext import db


class Track(db.Model):
    author = db.StringProperty()
    lyric = db.TextProperty()
    number = db.IntegerProperty()
    ref = db.URLProperty()
    title = db.StringProperty()
    vol = db.IntegerProperty()
    created = db.DateTimeProperty()
    updated = db.DateTimeProperty()
