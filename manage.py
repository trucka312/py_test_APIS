from flask_marshmallow import Marshmallow
from flask_script import Manager
from flask_migrate import Migrate
from application import run_app
from application.config.config_dev import ConfigDevelop
from application.server import app
from application.database import init_database, db
import sys
from os.path import abspath, dirname
sys.path.insert(0, dirname(abspath(__file__)))


def init_app():
    app.config.from_object(ConfigDevelop)
    init_database(app)


manager = Manager()
migrate = Migrate(app, db)
ma = Marshmallow(app)


@manager.command
def run():
    """ Starts server on port 8000. """
    run_app(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    run_app(host="0.0.0.0", port=8000, debug=True)