import logging
import requests
import json
from requests.auth import HTTPBasicAuth
from unomaly.group import Group
from unomaly.system import System

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
requests_log = logging.getLogger("urllib3")
requests_log.setLevel(logging.INFO)
requests_log.propagate = True


class Api(object):
    def __init__(self, url, token=None, ssl_verify=True):
        self.url = url
        self.token = token
        self.ssl_verify = ssl_verify

        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth('api', token)
        self.session.verify = self.ssl_verify
        self.session.headers = {'Content-Type': 'application/json'}

    def get(self, url):
        req = self.session.get(url)
        resp = req.json()
        if req.ok:
            if resp['error'] is not False:
                raise UnomalyApiError(f"Got error from API: {resp['error']}")
            return resp['data']
        else:
            raise RequestError(req)

    def post(self, url, data=None):
        req = self.session.post(url, data=data)
        resp = req.json()
        if req.ok:
            if resp['error'] is not False:
                raise UnomalyApiError(f"Got error from API: {resp['error']}")
            return resp['data']
        else:
            raise RequestError(req)

    def put(self, url, data=None):
        req = self.session.put(url, data=data)
        resp = req.json()
        if req.ok:
            if resp['error'] is not False:
                raise UnomalyApiError(f"Got error from API: {resp['error']}")
            return resp['data']
        else:
            raise RequestError(req)

    def get_all_groups(self):
        resp = self.get(f'{self.url}/restapi/groups')
        ret = []
        for i in resp:
            id = i['id']
            del i['id']
            name = i['name']
            del i['name']

            ret.append(Group(self, id, name, **i))

        return ret

    def get_all_systems(self):
        resp = self.get(f'{self.url}/restapi/systems')
        ret = []
        for i in resp:
            id = i['id']
            del i['id']
            name = i['name']
            del i['name']

            ret.append(System(self, id, name, **i))

        return ret

    def create_group(self, name, parent_id=None):
        data = {
            'name': name,
            'displayName': name
        }
        if parent_id is not None:
            data['parent_id'] = int(parent_id)

        resp = self.post(
            f'{self.url}/restapi/groups',
            data=json.dumps(data)
        )
        return int(resp['id'])


class RequestError(Exception):
    def __init__(self, message):
        req = message

        if req.status_code == 404:
            message = "The requested url: {} could not be found.".format(
                req.url
            )
        else:
            try:
                message = "The request failed with code {} {}: {}".format(
                    req.status_code, req.reason, req.json()
                )
            except ValueError:
                message = (
                    "The request failed with code {} {} but more specific "
                    "details were not returned in json.".format(
                        req.status_code, req.reason
                    )
                )

        super(RequestError, self).__init__(message)
        self.req = req
        self.request_body = req.request.body
        self.url = req.url
        self.error = req.text


class UnomalyApiError(Exception):
    def __init__(self, message):
        super(UnomalyApiError, self).__init__(message)
