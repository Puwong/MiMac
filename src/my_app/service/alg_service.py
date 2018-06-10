import os

from flask import g
from .base_service import BaseService
from .user_service import UserService
from my_app.common.db_helper import exists_query
from my_app.common.tools import create_dir_loop
from my_app.common.constant import AppConfig
from my_app.models import Alg, AlgUserRelationship


class AlgService(BaseService):

    model = Alg

    def get_all(self, **kwargs):
        return super(AlgService, self).get_all(delete=False, **kwargs)

    def get_alg_path(self, id_or_ins):
        return AppConfig.ALG_DIR + '/' + str(self.get(id_or_ins).id)

    def get_my_alg_ids(self, with_title=False):
        me = UserService(self.db).get(g.user_id)
        if with_title:
            return {i.alg_id: i.alg.title for i in me.algs}
        return [i.alg_id for i in me.algs]

    def create(self, **kwargs):
        alg = self.model(**kwargs)
        self.db.session.add(alg)
        self.db.session.commit()
        alg_path = self.get_alg_path(alg.id)
        create_dir_loop(alg_path)
        return alg

    def delete(self, id_or_ins):
        alg = self.get(id_or_ins)
        alg.delete = True
        self.db.session.commit()

    def add2user(self, a_id):
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


