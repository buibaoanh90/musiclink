import logging
import urllib

from app import utils
from app.interfaces import Flow, Chain, Processor
from app.services.datastore import TrackDataSource, Bulk


class TracksFeed(Flow):
    def __init__(self):
        Flow.__init__(self)
        pass

    def run(self):
        chain = Chain()
        feed = FeedBuilder()
        chain.add(feed)
        ds = TrackDataSource()
        ds.save(chain)
        return feed.list()


class FeedBuilder(Processor):
    SEARCH_URL = 'http://m.nhaccuatui.com/tim-kiem'

    def __init__(self):
        Processor.__init__(self)
        self.urls = []
        pass

    def process(self, track):
        title = track.title
        title = utils.strip_accents(title)
        query = {'q' : title}
        url = FeedBuilder.SEARCH_URL + '?' + urllib.urlencode(query) + '\r\n'
        self.urls.append(url)

    def list(self):
        return ''.join(self.urls)
