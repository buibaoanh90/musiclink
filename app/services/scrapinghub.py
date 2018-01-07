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

    def __init__(self, spider_id, job_id):
        self.spider_id = spider_id
        self.job_id = job_id

    def get_endpoint(self, name, count, start, fmt):
        path = utils.build_path([name, API.PROJECT_ID, self.spider_id, self.job_id])
        params = {
            'apikey': API.KEY,
            'count': str(count),
            'start': utils.build_path([API.PROJECT_ID, self.spider_id, self.job_id, str(start)]),
            'format': fmt
        }
        return utils.build_url(API.BASE_URL, path, params)


class ItemDataSource(DataSource):
    MAX_SIZE = 1000000

    def __init__(self, api):
        DataSource.__init__(self)
        self.api = api

    def save(self, processor, limit = -1):
        if limit <= 0:
            limit = self.MAX_SIZE
        for i in range(1, limit, configs.SCROLL_SIZE):
            response = self.scroll(i, min(limit - i + 1, configs.SCROLL_SIZE))

            jsons = json.loads(response)
            if len(jsons) == 0:
                break
            for js in jsons:
                processor.process(js)

    def scroll(self, i, size):
        endpoint = self.api.get_endpoint(
            API.ITEMS,
            size,
            i,
            API.JL
        )
        response = utils.fetch_url(endpoint)
        return response


class TrackDataSource(ItemDataSource):
    def __init__(self):
        ItemDataSource.__init__(self, API('1', '9'))


class ArtistDataSource(ItemDataSource):
    def __init__(self):
        ItemDataSource.__init__(self, API('2', '3'))
