import ujson as json
from numbers import Integral
from sqlalchemy import or_
from sqlalchemy.orm.attributes import QueryableAttribute


class BaseService(object):

    def __init__(self, db):
        self.db = db
        self.model = getattr(self, 'model', None)
        self.int_keys = getattr(self, 'int_keys', [])
        self.json_keys = getattr(self, 'json_keys', [])
        self.search_fields = getattr(self, 'search_fields', [])
        self.sort_fields = getattr(self, 'sort_fields', [])

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

    def apply_search(self, query, search):
        filters = list()
        for field_name in getattr(self, 'search_fields', []):
            pf_name = 'prepare_search_{}'.format(field_name)
            if hasattr(self, pf_name):
                pf = getattr(self, pf_name)
                filters.extend(pf(search))
        if query:
            if filters:
                query = query.filter(or_(*filters))
        # return [cls.model.id.in_(ids)] if ids else []
        return query

    def apply_sorts(self, query, sorts):
        if sorts:
            assert isinstance(sorts, list), 'sorts must be list'
        _sorts = []
        for name, reverse in sorts:
            if (isinstance(getattr(self.model, name, None), QueryableAttribute) and
                    hasattr(self, 'sort_fields') and self.sort_fields and
                    name in self.sort_fields):
                sort = getattr(self.model, name).desc() if reverse else getattr(self.model, name).asc()  # NOQA
                _sorts.append(sort)
        if query:
            query = query.order_by(*_sorts)
        return query, _sorts

    def query_update(self, query, **kwargs):
        if 'sort' in kwargs.keys():
            query, _ = self.apply_sorts(query, kwargs['sort'])
        if 'search' in kwargs.keys():
            query = self.apply_search(query, kwargs['search'])
        return query

    def get_all(self, **kwargs):
        query = self.model.query
        for key in kwargs:
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == kwargs[key])
        query = self.query_update(query, **kwargs)
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

        query = self.query_update(model.query, **kwargs)
        for key in kwargs:
            if hasattr(model, key):
                query = query.filter(getattr(model, key) == kwargs[key])

        return query.first()

    def get(self, *args, **kwargs):
        return self.get_by(*args, **kwargs)

