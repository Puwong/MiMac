from numbers import Integral


class BaseService(object):

    def __init__(self, db):
        self.db = db
        self.model = getattr(self, 'model', None)

    def get_all(self, with_delete=True):
        query = self.model.query
        if not with_delete:
            query = query.filter(self.model.delete==False)
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

