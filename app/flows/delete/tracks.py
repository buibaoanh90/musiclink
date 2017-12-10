from app.interfaces import Flow, Chain, Processor
from app.services.datastore import TrackDataSource, Bulk


class Tracks(Flow):
    def __init__(self):
        Flow.__init__(self)
        pass

    def run(self):
        chain = Chain()
        chain.add(Storage())
        ds = TrackDataSource()
        ds.save(chain, 1000)
        Bulk.get_instance().flush_all()


class Storage(Processor):

    def __init__(self):
        Processor.__init__(self)
        pass

    def process(self, track):
        bulk = Bulk.get_instance()
        bulk.delete(track)
