# -*- coding: utf-8 -*-

from flask.ext.script import Server, Shell, Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from my_app import app, app_conf
from my_app.foundation import db
from my_app.models import User, Team, TeamUserRelationship, Alg
from my_app.service import UserService
from my_app.common.tools import remove_dir_loop, create_dir_loop
from my_app.common.constant import BaseAlgorithm, UserRole


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server('0.0.0.0', port=22232))
manager.add_command('db', MigrateCommand)


def _add_root():
    root_user = User(username='root', password='123456', email='root@mimac.com', role=UserRole.ADMIN)
    tr = TeamUserRelationship(isLeader=True)
    tr.team = Team(title='root_team')

    root_user.teams.append(tr)
    db.session.add(root_user)
    db.session.commit()
    UserService(db).add_user_dir(root_user.id)


def _add_alg():
    db.session.add(Alg(title='b_c_basic', base=BaseAlgorithm.BiClass))
    db.session.add(Alg(title='m_c_basic', base=BaseAlgorithm.MulClass))
    db.session.add(Alg(title=u'猫狗二分类', base=BaseAlgorithm.BiClass))
    db.session.add(Alg(title=u'肺癌检测', base=BaseAlgorithm.MulClass))
    db.session.commit()


@manager.command
def dropall():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()
        remove_dir_loop(app_conf('USER_DIR'))


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

