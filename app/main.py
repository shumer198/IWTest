import logging
from flask import Flask, render_template
import os
from settings import data_folder, file_name
import json
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

    @app.before_first_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/", methods=["GET"])
    def get_main_page():
        from models import db, get_quotes_from_csv, \
            load_quotes_to_db, get_quotes_with_seasonality, get_quotes_from_db

        file_path = os.path.join(data_folder, file_name)
        quotes = get_quotes_from_csv(file_path=file_path)
        quotes_with_seasonality = get_quotes_with_seasonality(quotes=quotes)
        load_quotes_to_db(quotes=quotes_with_seasonality)


        quotes = get_quotes_from_db()
        return render_template('index.html', quotes=quotes)

        # date, close, seasonality = get_quotes_from_db()

        # return render_template('index.html',
        #                        dt=json.dumps(date),
        #                        close=close,
        #                        seasonality=seasonality)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

    # from models import db, get_quotes_from_csv,\
    #     load_quotes_to_db, get_quotes_with_seasonality, get_quotes_from_db
    #
    # file_path = os.path.join(data_folder, file_name)
    # quotes = get_quotes_from_csv(file_path=file_path)
    # quotes_with_seasonality = get_quotes_with_seasonality(quotes=quotes)
    # load_quotes_to_db(quotes=quotes_with_seasonality)

