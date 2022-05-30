import logging

import pandas as pd
from flask import Flask
from load_quotes import get_dataframe_from_csv
import os
from settings import data_folder, file_name
from sqlalchemy import delete


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql+psycopg2://admin:admin@localhost/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = True

    from models.models import (
        Quote,
        get_quotes_for_market,
        db
    )

    db.init_app(app)

    @app.before_first_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/", methods=["GET"])
    def get_main_page():
        file_path = os.path.join(data_folder, file_name)
        quotes = pd.DataFrame()
        try:
            quotes = get_dataframe_from_csv(file_path=file_path)
        except Exception as exc:
            logger.error(f'Data loading error {exc}')

        if not quotes.empty:
            quotes.to_sql('quotes', db.engine, if_exists='replace')
            db.session.commit()
        return "ok"

    @app.route("/quotes/<market>", methods=["GET"])
    def get_quotes(market):
        return get_quotes_for_market(market=market)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
