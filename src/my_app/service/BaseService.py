from numbers import Integral


class BaseService(object):

    def __init__(self, db):
        self.db = db
        self.model = getattr(self, 'model', None)

    def get_by(self, *args, **kwargs):
        model = self.model

        if args and args[0]:
            id_or_ins = args[0]
            if isinstance(id_or_ins, model):
                return id_or_ins
            elif isinstance(id_or_ins, Integral):
                return model.query.get(int(id_or_ins))
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

