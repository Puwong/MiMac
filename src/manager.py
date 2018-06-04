# -*- coding: utf-8 -*-
import os
import ujson as json
from shutil import copyfile
from flask.ext.script import Server, Shell, Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from my_app import app, app_conf
from my_app.foundation import db
from my_app.models import User, Team, TeamUserRelationship, Alg
from my_app.service import UserService, AlgService
from my_app.common.tools import remove_dir_loop, create_dir_loop
from my_app.common.constant import BaseAlgorithm, UserRole


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server('0.0.0.0', port=22232))
manager.add_command('db', MigrateCommand)


def _add_root():
    root_pwd = UserService.generate_pwd('123456')
    root_user = User(username='root', password=root_pwd, email='root@mimac.com', role=UserRole.ADMIN)
    tr = TeamUserRelationship(isLeader=True)
    tr.team = Team(title='root_team')

    root_user.teams.append(tr)
    db.session.add(root_user)
    db.session.commit()
    UserService(db).add_user_dir(root_user.id)


def _add_alg():
    from my_app.common.tools import get_alg_path
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
    alg_path = get_alg_path(cd_alg)
    print alg_path
    copyfile(alg_path + '/../../deeplearn/b_c_basic.json', alg_path + '/model.json')
    copyfile(alg_path + '/../../deeplearn/b_c_cat_dog.h5', alg_path + '/weight.h5')


@manager.command
def dropall():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()
        remove_dir_loop(app_conf('USER_DIR'))
        remove_dir_loop(app_conf('ALG_DIR'))


@manager.command
def createall():
    "Creates database tables"
    db.create_all()
    db.session.commit()
    create_dir_loop(app_conf('USER_DIR'))
    create_dir_loop(app_conf('ALG_DIR'))
    _add_root()
    _add_alg()


@manager.command
def resetall():
    dropall()
    createall()


if __name__ == "__main__":
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    manager.run()

