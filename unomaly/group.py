from datetime import datetime


class Group(object):
    def __init__(self, client, id, name, **kwargs):
        self.client = client
        self.id = id
        if len(name) < 1:
            raise("Group name cannot be < 1 chars")
        else:
            self.name = name
            self.display_name = name
            self.created = kwargs['created']
            self.updated = kwargs['updated']
            self.parent_id = kwargs['parent_id']

    def __repr__(self):
        items = ("%s = %r" % (k, v) for k, v in self.__dict__.items())
        return "<%s: {%s}>" % (self.__class__.__name__, ', '.join(items))

    def has_parent(self):
        if self.parent_id is not None:
            return True
        return False

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, v):
        self._id = int(v)

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
    def parent_id(self):
        return self._parent_id

    @parent_id.setter
    def parent_id(self, v):
        if v is not None:
            self._parent_id = int(v)
        else:
            self._parent_id = None
