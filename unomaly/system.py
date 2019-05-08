import socket
import json
from datetime import datetime


class System(object):
    def __init__(self, client, id, name, **kwargs):
        self.client = client
        self.id = id
        if len(name) < 1:
            raise("Name cannot be < 1 chars")

        self.name = name
        self.alias = kwargs['alias']

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, v):
        self._id = int(v)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, v):
        self._name = str(v)

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, v):
        self._alias = str(v)

    @property
    def created(self):
        return self._created

    @created.setter
    def created(self, v):
        self._created = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ")

    @property
    def updated(self):
        return self._updated

    @updated.setter
    def updated(self, v):
        self._updated = datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%fZ")

    @property
    def groups(self):
        ret = self.client.get(f'{self.client.url}/restapi/systems/{self.id}')['groups']
        if not len(ret):
            return None
        return ret

    def add_to_group(self, group_id):
        # Apparently PUT is used to delete... so we're POSTing here instead
        resp = self.client.post(
            f'{self.client.url}/restapi/groupssystems',
            data=json.dumps({
                'group_id': group_id,
                'system_ids': [self.id]
            })
        )
        return resp
