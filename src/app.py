import os
from flask import Flask
from src.database import init_db
from src import routes


def create_app(test_config=None):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = 'taskflow-secreto'

    if test_config:
        app.config.update(test_config)

    if app.config.get('DATABASE_PATH'):
        os.environ['TASKFLOW_DB_PATH'] = str(app.config['DATABASE_PATH'])

    init_db()
    app.register_blueprint(routes.bp)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
