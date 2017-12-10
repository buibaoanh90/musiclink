import webapp2
import logging
from google.appengine.api import taskqueue
from app.flows.sync.tracks import Tracks


class SyncTracks(webapp2.RequestHandler):
    def post(self):
        logging.info('sync start')

        flow = Tracks()
        flow.run()

        logging.info('sync finished')

    def get(self):
        logging.info('task start')
        task = taskqueue.add(
            url='/sync-tracks',
            target='worker',
            name='sync-tracks'
        )
        logging.info('sync finished')
        self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))
