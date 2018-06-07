import ujson as json
from numbers import Integral


class BaseService(object):

    def __init__(self, db):
        self.db = db
        self.model = getattr(self, 'model', None)
        self.int_keys = getattr(self, 'int_keys', [])
        self.json_keys = getattr(self, 'json_keys', [])

    def get_info(self, *args, **kwargs):
        item = self.get(*args, **kwargs)
        info = {}
        if item:
            model_keys = self.model.__table__.columns.keys()
            for key in model_keys:
                if key in self.json_keys:
                    value = json.loads(getattr(item, key))
                else:
                    value = getattr(item, key, None)
                info[key] = value
        for key in self.int_keys:
            if key in info:
                info[key] = int(info[key] or 0)
        return info

    def get_all(self, **kwargs):
        query = self.model.query
        for key in kwargs:
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == kwargs[key])
        return query.all()

    def get_by(self, *args, **kwargs):
        model = self.model

        if args and args[0]:
            id_or_ins = args[0]
            if isinstance(id_or_ins, model):
                return id_or_ins
            elif isinstance(id_or_ins, Integral):
                return model.query.get(id_or_ins)
            else:
                return None
        else:
            if len(kwargs) == 0:
                return None
        query = model.query
        for key in kwargs:
            if hasattr(model, key):
                query = query.filter(getattr(model, key) == kwargs[key])

        return query.first()

    def get(self, *args, **kwargs):
        return self.get_by(*args, **kwargs)

