import urllib2
import logging


def fetch_url(url):
    response = ''
    try:
        result = urllib2.urlopen(url)
        response = result.read()
    except urllib2.URLError:
        logging.exception('Caught exception fetching url')
    return response
