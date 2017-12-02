import requests


class AriangSite():
    DOMAIN = 'http://arirang.com.vn'
    LINKS = [
        'tai-ve_1_1.html',
        'tai-ve_1_2.html',
        'tai-ve_1_3.html',
    ]


class AriangScraper():

    def fetch_url(self, url):
        response = requests.get(url)
        return response.text
