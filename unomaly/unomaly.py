import requests
from requests.auth import HTTPBasicAuth

class API(object):
    def __init__(self, url, token=None, ssl_verify=True):
        self.url = url
        self.token = token
        self.ssl_verify = ssl_verify

        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth('api', token)
        self.session.verify = self.ssl_verify
        