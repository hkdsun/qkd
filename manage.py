from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import app, db
app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, db)
manager = Manager(app)
shell = Shell(use_ipython=True)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
