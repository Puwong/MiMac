
from flask.ext.script import Server, Shell, Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

from my_app import app
from my_app.foundation import db


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server('0.0.0.0', port=22232))
manager.add_command('db', MigrateCommand)


@manager.command
def dropall():
    "Drops all database tables"
    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


@manager.command
def createall():
    "Creates database tables"
    db.create_all()
    db.session.commit()


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

