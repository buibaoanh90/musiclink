import webapp2
import logging
from app.services import ariang


class SyncTracks(webapp2.RequestHandler):
    def get(self):
        logging.info('start syncing')
        scraper = ariang.AriangScraper()

        self.response.write('start syncing: ' + scraper.fetch_url(ariang.AriangSite.DOMAIN + '/' + ariang.AriangSite.LINKS[0]))