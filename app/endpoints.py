import webapp2
import logging

from app.flows.sync.tracks import Tracks


class SyncTracks(webapp2.RequestHandler):
    def get(self):
        logging.info('start syncing')

        flow = Tracks()
        flow.run()

        self.response.write('finished syncing: ')
