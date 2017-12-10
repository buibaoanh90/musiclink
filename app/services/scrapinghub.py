import StringIO
import json
from app.interfaces import DataSource
from app.models import Track
from app import utils, configs


class API:
    JL = 'json'
    PROJECT_ID = '261462'
    KEY = 'f5914a42b48f467d96aa4e9db431f1b5'
    ITEMS = 'items'
    BASE_URL = 'https://storage.scrapinghub.com'
    STATS = 'stats'

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

    def __init__(self, spider_id, job_id):
        DataSource.__init__(self)
        self.spider_id = spider_id
        self.job_id = job_id

    def save(self, processor, limit = -1):
        if limit < 0:
            limit = self.MAX_SIZE
        for i in range(1, limit, configs.SCROLL_SIZE):
            response = self.scroll(i, min(limit - i + 1, configs.SCROLL_SIZE))
            jsons = json.loads(response)
            if len(jsons) == 0:
                break
            for js in jsons:
                processor.process(js)

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
