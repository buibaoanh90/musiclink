# coding=utf-8
from app.interfaces import Processor, Flow, Chain
from app.models import Track
from app.services.datastore import Bulk
from app.services.scrapinghub import TrackDataSource


class Tracks(Flow):
    def __init__(self):
        Flow.__init__(self)
        pass

    def run(self):
        chain = Chain()
        chain.add(Transformer()).add(Validator()).add(Normalizer()).add(Popularity()).add(Storage())
        ds = TrackDataSource()
        ds.save(chain, 1000)
        Bulk.get_instance().flush_all()


class Transformer(Processor):
    AUTHOR = 'author'
    LYRIC = 'lyric'
    NUMBER = 'number'
    REF = 'ref'
    TITLE = 'title'
    URL = 'url'
    VOL = 'vol'

    def __init__(self):
        Processor.__init__(self)
        pass

    def process(self, json):
        item = self.transform(json)
        self.process_next(item)

    def transform(self, json):
        return Track(
            author=json.get(self.AUTHOR, [''])[0],
            lyric=json.get(self.LYRIC, [''])[0],
            number=int(json[self.NUMBER][0]),
            ref=json.get(self.REF, [None])[0],
            title=json[self.TITLE][0],
            vol=int(json.get(self.VOL, [0])[0]) if json.get(self.VOL, [0])[0] is not None else 0
        )


class Normalizer(Processor):
    REDUNDANT_TEXT = u'lời bài hát'

    def __init__(self):
        Processor.__init__(self)
        pass

    def process(self, track):
        track.lyric = track.lyric.replace(Normalizer.REDUNDANT_TEXT, u'')
        self.process_next(track)


class Storage(Processor):

    def __init__(self):
        Processor.__init__(self)
        pass

    def process(self, track):
        # logging.info(track.lyric)
        # logging.info(track.author)
        # logging.info(track.number)
        # logging.info(track.title)
        # logging.info(track.ref)
        # logging.info(track.vol)
        bulk = Bulk.get_instance()
        bulk.add(track)


class Validator(Processor):
    def __init__(self):
        Processor.__init__(self)
        pass

    def process(self, track):
        self.process_next(track)


class Popularity(Processor):
    def __init__(self):
        Processor.__init__(self)
        pass

    def process(self, track):
        self.process_next(track)
