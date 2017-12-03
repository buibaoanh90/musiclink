import webapp2
import logging
from app.services import ariang
from app.services.ariang import Factory


class SyncTracks(webapp2.RequestHandler):
    def get(self):
        logging.info('start syncing')

        ds = Factory().get_data_source()
        ds.load()
        it = ds.get_iterator()
        out = []
        while True:
            try:
                val = it.next()
                out.append(val)
                print(val)
            except StopIteration:
                print("Iteration done.")
                break

        self.response.write('start syncing: ' + str(out))