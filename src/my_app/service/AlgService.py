import os

from flask import g
from .BaseService import BaseService
from my_app.models import Alg, AlgUserRelationship


class AlgService(BaseService):

    model = Alg

    def get_all(self, with_delete=False):
        return super(AlgService, self).get_all(with_delete=with_delete)

    def get_my_alg_ids(self, with_title=False):
        from .UserService import UserService
        me = UserService(self.db).get(g.user_id)
        if with_title:
            return {i.alg_id: i.alg.title for i in me.algs}
        return [i.alg_id for i in me.algs]

    def create(self, **kwargs):
        from my_app.common.tools import create_dir_loop, get_alg_path
        alg = self.model(**kwargs)
        self.db.session.add(alg)
        self.db.session.commit()
        alg_path = get_alg_path(alg.id)
        create_dir_loop(alg_path)
        return alg

    def delete(self, id_or_ins):
        alg = self.get(id_or_ins)
        alg.delete = True
        self.db.session.commit()

    def add2user(self, a_id):
        from .UserService import UserService
        from my_app.common.db_helper import exists_query
        alg = AlgService(self.db).get(a_id)
        print alg.id, a_id
        if not alg or exists_query(AlgUserRelationship.query.filter(
                AlgUserRelationship.user_id==g.user_id).filter(AlgUserRelationship.alg_id==alg.id)) or alg.id != a_id:
            return False
        user = UserService(self.db).get(g.user_id)
        relation = AlgUserRelationship()
        relation.alg = alg
        user.algs.append(relation)
        print user, alg, relation
        self.db.session.commit()


