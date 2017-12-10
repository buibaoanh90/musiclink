import StringIO
import json
from app.interfaces import DataSource
from app.models import Track
from app import utils


class API:
    JL = 'jl'
    PROJECT_ID = '261462'
    KEY = 'f5914a42b48f467d96aa4e9db431f1b5'
    ITEMS = 'items'
    BASE_URL = 'https://storage.scrapinghub.com'

    def __init__(self):
        pass

    @staticmethod
    def get_endpoint(name, spider_id, job_id, count, start, fmt):
        path = utils.build_path([name, API.PROJECT_ID, spider_id, job_id])
        params = {
            'apikey': API.KEY,
            'count': str(count),
            'start': utils.build_path([API.PROJECT_ID, spider_id, job_id, str(start)]),
            'format': fmt
        }
        return utils.build_url(API.BASE_URL, path, params)


class TrackDataSource(DataSource):
    MAX_SIZE = 1000000
    SCROLL_SIZE = 100

    def __init__(self):
        DataSource.__init__(self)
        self.spider_id = '1'
        self.job_id = '7'

    def save(self, processor, limit = -1):
        if limit < 0:
            limit = self.MAX_SIZE
        for i in range(1, limit, TrackDataSource.SCROLL_SIZE):
            response = self.scroll(i, min(limit - i, TrackDataSource.SCROLL_SIZE))
            if len(response) < 0:
                break
            self.read(response, processor)

    def read(self, response, processor):
        buf = StringIO.StringIO(response)
        line = buf.readline()
        while len(line) > 0:
            js = json.loads(line)
            processor.process(js)
            line = buf.readline()
        buf.close()

    def scroll(self, i, size):
        endpoint = API.get_endpoint(
            API.ITEMS,
            self.spider_id,
            self.job_id,
            size,
            i,
            API.JL
        )
        response = utils.fetch_url(endpoint)
        return response
