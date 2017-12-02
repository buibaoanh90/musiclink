import webapp2
import logging

class ImportTracks(webapp2.RequestHandler):
    def get(self):
        logging.info('start importing')
        self.response.write('start importing')