import webapp2
import logging
from google.appengine.api import taskqueue
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