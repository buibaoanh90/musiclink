import webapp2
import logging
from google.appengine.api import taskqueue

from app.flows.query.tracks_feed import TracksFeed as TracksFeedFlow
from app.flows.sync.tracks import Tracks as SyncTracksFlow
from app.flows.delete.tracks import Tracks as DeleteTracksFlow


class SyncTracks(webapp2.RequestHandler):
    def post(self):
        logging.info('sync start')
        flow = SyncTracksFlow()
        flow.run()
        logging.info('sync finished')

    def get(self):
        logging.info('task start')
        task = taskqueue.add(
            url='/tasks/sync-tracks',
            target='worker'
        )
        logging.info('task finished')
        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))


class DeleteTracks(webapp2.RequestHandler):
    def post(self):
        logging.info('delete start')
        flow = DeleteTracksFlow()
        flow.run()
        logging.info('delete finished')

    def get(self):
        logging.info('task start')
        task = taskqueue.add(
            url='/tasks/delete-tracks',
            target='worker'
        )
        logging.info('task finished')
        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))


class Test(webapp2.RequestHandler):
    def post(self):
        logging.info('test start')
        flow = TracksFeedFlow()
        flow.run()
        logging.info('test finished')

    def get(self):
        logging.info('task start')
        task = taskqueue.add(
            url='/tasks/test',
            target='worker'
        )
        logging.info('task finished')
        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))


class TracksFeed(webapp2.RequestHandler):
    def get(self):
        logging.info('get tracks feed')
        flow = TracksFeedFlow()
        urls = flow.run()
        logging.info('feed is built')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Content-Disposition'] = "attachment; filename=urls.txt"
        self.response.write(urls)
