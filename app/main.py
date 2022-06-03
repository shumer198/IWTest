import logging

from flask import Flask, make_response, render_template
from flask_restx import Api, Resource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://admin:admin@localhost/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True

    from models import db, get_quotes_from_db

    db.init_app(app)

    api = Api(app)

    @api.route("/seasonality")
    class Seasonality(Resource):
        @staticmethod
        def get():
            """
            Return web page with seasonal chart
            """
            quotes = get_quotes_from_db()
            resp = make_response(render_template("index.html", quotes=quotes))
            resp.headers["Content-type"] = "text/html; charset=utf-8"
            return resp

    api.add_resource(Seasonality)

    @app.before_first_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
