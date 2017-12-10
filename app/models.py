from google.appengine.ext import db


class Track(db.Model):
    author = db.StringProperty()
    lyric = db.TextProperty()
    number = db.IntegerProperty()
    ref = db.URLProperty()
    title = db.StringProperty()
    vol = db.IntegerProperty()
    created = db.DateTimeProperty()

    def __init__(self, author, lyric, number, ref, title, vol, parent=None, key_name=None):
        db.Model.__init__(self, parent, key_name)
        self.author = author
        self.lyric = lyric
        self.number = number
        self.ref = ref
        self.title = title
        self.vol = vol
