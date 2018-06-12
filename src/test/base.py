# -*- coding: utf-8 -*-
import unittest
import tempfile
import ujson as json
# from pyquery import PyQuery as pq
# https://www.cnblogs.com/iamjqy/p/6824444.html
from flask import url_for
from shutil import copyfile
from my_app import app
from my_app.foundation import db
from my_app.models import User, Team, TeamUserRelationship
from my_app.service import UserService, AlgService
from my_app.common.constant import BaseAlgorithm, AppConfig, UserRole
from my_app.common.tools import create_dir_loop, remove_dir_loop


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.app = app
        self.client = app.test_client()
        self.client.testing = True
        self.init_db()

    def faster_url_for(self, endpoint):
        # TODO cannot transport values
        return self.app.url_map._rules_by_endpoint[endpoint][0].rule

    def url_for_(self, endpoint, **kwargs):
        with self.app.test_request_context('/'):
            print url_for(endpoint, **kwargs)
            return url_for(endpoint, **kwargs)

    @staticmethod
    def _add_root():
        root_pwd = UserService.generate_pwd('123456')
        root_user = User(username='root', password=root_pwd, email='root@mimac.com', role=UserRole.ADMIN)
        tr = TeamUserRelationship(isLeader=True)
        tr.team = Team(title='root_team')

        root_user.teams.append(tr)
        db.session.add(root_user)
        db.session.commit()
        UserService(db).add_user_dir(root_user.id)

    @staticmethod
    def _add_alg():
        cd_alg = AlgService(db).create(title=u'猫狗二分类', base=BaseAlgorithm.BiClass, config=json.dumps({
            'class_cnt': 2,
            'labels': [u'这是一只猫', u'这是一条狗']
        }))
        AlgService(db).create(title=u'肺部CT图像肺结节良恶性诊断', base=BaseAlgorithm.BiClass, config=json.dumps({
            'class_cnt': 2,
            'labels': [u'良性肺结节', u'恶性肺结节']
        }))
        AlgService(db).create(title=u'乳腺钼靶X线图像良恶性诊断', base=BaseAlgorithm.BiClass, config=json.dumps({
            'class_cnt': 2,
            'labels': [u'良性乳腺', u'恶性乳腺']
        }))
        alg_path = AlgService(db).get_alg_path(cd_alg)
        copyfile(alg_path + '/../../deeplearn/b_c_basic.json', alg_path + '/model.json')
        copyfile(alg_path + '/../../deeplearn/b_c_cat_dog.h5', alg_path + '/weight.h5')

    @staticmethod
    def init_db():
        db.drop_all()
        remove_dir_loop(AppConfig.USER_DIR)
        remove_dir_loop(AppConfig.ALG_DIR)

        db.create_all()
        db.session.commit()
        create_dir_loop(AppConfig.USER_DIR)
        create_dir_loop(AppConfig.ALG_DIR)
        BaseTestCase._add_root()
        BaseTestCase._add_alg()

    def tearDown(self):
        try:
            db.drop_all()
        except Exception:
            import os
            db_file = os.path.join(app.config['BASEDIR'], 'app2.db')
            if os.path.exists(db_file):
                os.remove(db_file)

    def ping_bak(self, url, method='get', data=None):
        ret = lambda: None
        setattr(ret, 'status', '500 ERROR')
        setattr(ret, 'data', dict())
        if hasattr(self.client, method):
            func = getattr(self.client, method)
            rv = func(url, data, follow_redirects=True)
            ret.status = rv.status
            if hasattr(rv, data):
                ret.data = rv.data
                # ret.data = json.loads(rv.data)  # TODO after front and rear separation
        return ret

    def ping(self, url, method='get', **kwargs):
        func = getattr(self.client, method)
        return func(url, follow_redirects=True, **kwargs)

    def login(self, username, password):
        return self.ping(self.url_for_('Auth.login'), 'post', data=dict(
            username=username,
            password=password
        ))

    def logout(self):
        return self.ping(self.url_for_('Auth.login'))

    def register(self, username, password, email):
        return self.ping(self.url_for_('Auth.register'), 'post', data=dict(
            username=username,
            password=password,
            email=email
        ))

    def test_auth(self):
        rv = self.register('1', '1', '1@163.com')
        self.assertEqual(rv.status, '200 OK')
        rv = self.login('1', '1')
        self.assertEqual(rv.status, '200 OK')
        rv = self.logout()
        self.assertEqual(rv.status, '200 OK')

    def test_login(self):
        rv = self.login('root', '123456')
        self.assertEqual(rv.status, '200 OK')
        rv = self.logout()
        self.assertEqual(rv.status, '200 OK')
