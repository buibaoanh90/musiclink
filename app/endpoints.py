import webapp2
import logging
from app.services import ariang


class SyncTracks(webapp2.RequestHandler):
    def get(self):
        logging.info('start syncing')
        scraper = ariang.Scraper()
        # url = 'http://www.google.com/humans.txt'
        url = ariang.Site.DOMAIN + '/' + ariang.Site.LINKS[0]

        self.response.write('start syncing: ' + scraper.fetch_url(url))