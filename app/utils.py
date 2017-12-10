import urllib2
import logging
import urllib
import urlparse


def fetch_url(url):
    response = ''
    try:
        result = urllib2.urlopen(url)
        response = result.read()
    except urllib2.URLError:
        logging.exception('Caught exception fetching url')
    return response


def build_url(base_url, path, args_dict):
    # Returns a list in the structure of urlparse.ParseResult
    url_parts = list(urlparse.urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urllib.urlencode(args_dict)
    return urlparse.urlunparse(url_parts)


def build_path(parts):
    return reduce(lambda x, y: x + '/' + y, parts)


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z
