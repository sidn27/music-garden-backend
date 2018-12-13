from flask_migrate import MigrateCommand
from app import create_app
import os
from flask_script import Manager
from flask_script import Server
import config

hostenv = os.environ.get('HOSTENV') or 'default'

app = create_app(hostenv)
manager = Manager(app)
manager.add_command("runserver", Server(host="127.0.0.1", port=config.PORT))
manager.add_command("db", MigrateCommand)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()