import re
from app import utils
from app.interfaces import DataSource


class Site:
    def __init__(self):
        pass

    DOMAIN = 'http://arirang.com.vn'
    LINKS = [
        'tai-ve_1_1.html',
        'tai-ve_1_2.html',
        'tai-ve_1_3.html',
    ]
    PATTERN = r'window\.open\(\'(.+)\'\)'

    @staticmethod
    def format(url):
        return Site.DOMAIN + '/' + url


class Scraper:

    def __init__(self, pattern):
        self.pattern = pattern

    def scrape_page(self, url):
        page = utils.fetch_url(url)
        links = self.extract_links(page)
        return links

    def extract_links(self, page):
        matches = re.findall(self.pattern, page)
        return list(matches)


class TrackDataSource(DataSource):

    def __init__(self, scraper):
        DataSource.__init__(self)
        self.scraper = scraper
        self.data = []

    def load(self):
        pages = map(Site.format, Site.LINKS)
        self.data = reduce(lambda x, y: x + y,
                           [map(Site.format, self.scraper.scrape_page(page)) for page in pages])

    def get_iterator(self):
        print(len(self.data))
        return iter(self.data)


class Factory:
    def __init__(self):
        pass

    def get_scraper(self):
        scraper = Scraper(Site.PATTERN)
        return scraper

    def get_data_source(self):
        data_source = TrackDataSource(self.get_scraper())
        return data_source