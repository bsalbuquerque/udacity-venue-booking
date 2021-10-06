# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate


db = SQLAlchemy()
moment = Moment()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        import controllers

    return app


# Default port:
if __name__ == '__main__':
    create_app().run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''