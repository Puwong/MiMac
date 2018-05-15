import os
from flask.ext.script import Server, Shell, Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from my_app import app, app_conf
from my_app.foundation import db
from my_app.models import User, Team, TeamUserRelationship
from my_app.service import UserService
from my_app.common.db_helper import remove_dir_loop


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server('0.0.0.0', port=22232))
manager.add_command('db', MigrateCommand)

def _add_root():
    root_user = User(username='root', password='123456', email='root@mimac.com')
    tr = TeamUserRelationship(isLeader=True)
    tr.team = Team(title='root_team')

    root_user.teams.append(tr)
    db.session.add(root_user)
    db.session.commit()
    UserService().add_user_dir(root_user.id)

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
    os.mkdir(app_conf('USER_DIR'))
    _add_root()


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

