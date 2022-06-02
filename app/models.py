import logging
from typing import Any, Dict
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
# import matplotlib.pyplot as plt
from scipy import signal


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()


class Quote(db.Model):
    __tablename__ = "quote"

    market = db.Column(db.String(10), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    seasonality = db.Column(db.Float)
    __table_args__ = (
        db.UniqueConstraint("market", "date", name="unique_market_date"),
    )

    def __repr__(self):
        return f"Quotes {self.market} {self.date} {self.close}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def get_quotes_from_csv(file_path: str):
    try:
        header_list = ["market", "date", "open", "high", "low", "close"]
        quotes = pd.read_csv(file_path,
                             parse_dates=False, delimiter=',', decimal='.',
                             names=header_list)
        quotes['date'] = pd.to_datetime(quotes['date'], format='%m/%d/%Y')
    except Exception as e:
        logger.error(f'Data loading error. {e}')
        return 'Internal server error', 500

    return quotes


def load_quotes_to_db(quotes):
    if not quotes.empty:
        try:
            market = quotes.iloc[0][0]
            delete_quotes(market=market)
            quotes.to_sql('quote', con=db.engine, if_exists='append', index=False)
            db.session.commit()
        except Exception as e:
            logger.error(f'Cant load data to database. {e}')
            return 'Internal server error', 500

    return quotes


def delete_quotes(market):
    db.session.execute(delete(Quote).where(Quote.market == market))
    db.session.commit()


def get_seasonality(quotes):
    quotes['delta'] = quotes.close - quotes.close.shift(1)
    quotes.at[0, 'delta'] = 0
    quotes['day_of_year'] = pd.DatetimeIndex(quotes.date).day_of_year
    mean_delta = quotes.groupby('day_of_year')['delta'].mean()
    cumulative_sum = mean_delta.cumsum()
    seasonality = pd.DataFrame(cumulative_sum)
    seasonality['delta'] = signal.detrend(seasonality['delta'])
    # print(seasonality.to_string())
    # seasonal.plot()
    # plt.show()
    return seasonality


def get_quotes_with_seasonality(quotes):
    seasonality = get_seasonality(quotes=quotes)
    quotes['day_of_year'] = pd.DatetimeIndex(quotes.date).day_of_year
    quotes = quotes.merge(seasonality, on='day_of_year', how='left')
    quotes = quotes.drop(columns=['delta_x', 'day_of_year'])
    quotes = quotes.rename(columns={'delta_y': 'seasonality'})
    # print(quotes.to_string())

    return quotes


def get_quotes_from_db(market='KC-057'):
    quotes = db.session.query(Quote.date, Quote.close, Quote.seasonality).\
        filter(Quote.market == market).all()
    quotes_for_send = [[i, quote.close, quote.seasonality*5]
                       for i, quote in enumerate(quotes)]
    quotes_for_send.insert(0, ['Date', 'Close', 'Seasonality'])

    return quotes_for_send
