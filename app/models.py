import json
import logging
from typing import Any, Dict

import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from scipy import signal
from sqlalchemy import delete

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()


class Quote(db.Model):
    """
    Class describe quote table
    """

    __tablename__ = "quote"

    market = db.Column(db.String(10), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)
    seasonality = db.Column(db.Float)
    __table_args__ = (db.UniqueConstraint("market", "date", name="unique_market_date"),)

    def __repr__(self):
        return f"Quotes {self.market} {self.date} {self.close}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def get_quotes_from_csv(file_path: str):
    """

    :param file_path: path to file with quotes
    :return: quotes dataframe
    """
    try:
        header_list = ["market", "date", "open", "high", "low", "close"]
        quotes = pd.read_csv(
            file_path, parse_dates=False, delimiter=",", decimal=".", names=header_list
        )
        quotes["date"] = pd.to_datetime(quotes["date"], format="%m/%d/%Y")
    except Exception as e:
        logger.error(f"Data loading error. {e}")
        return "Internal server error", 500

    return quotes


def load_quotes_to_db(quotes):
    """
    Load quotes from dataframe to database
    :param quotes: dataframe of quotes
    """
    if not quotes.empty:
        try:
            market = quotes.iloc[0][0]
            delete_quotes(market=market)
            quotes.to_sql("quote", con=db.engine, if_exists="append", index=False)
            db.session.commit()
        except Exception as e:
            logger.error(f"Cant load data to database. {e}")
            return "Internal server error", 500

    return quotes


def delete_quotes(market):
    """
    Delete all quotes for market
    :param market: market for delete
    """
    db.session.execute(delete(Quote).where(Quote.market == market))
    db.session.commit()


def get_seasonality(quotes):
    """
    Return seasonality Series
    :param quotes: quotes dataframe
    """
    quotes["delta"] = quotes.close - quotes.close.shift(1)
    quotes.at[0, "delta"] = 0
    quotes["day_of_year"] = pd.DatetimeIndex(quotes.date).day_of_year
    mean_delta = quotes.groupby("day_of_year")["delta"].mean()
    cumulative_sum = mean_delta.cumsum()
    seasonality = pd.DataFrame(cumulative_sum)
    seasonality["delta"] = signal.detrend(seasonality["delta"])

    return seasonality


def get_quotes_with_seasonality(quotes):
    """
    Append seasonality series to quotes dataframe
    :param quotes: quotes dataframe
    """
    seasonality = get_seasonality(quotes=quotes)
    quotes["day_of_year"] = pd.DatetimeIndex(quotes.date).day_of_year
    quotes = quotes.merge(seasonality, on="day_of_year", how="left")
    quotes = quotes.drop(columns=["delta_x", "day_of_year"])
    quotes = quotes.rename(columns={"delta_y": "seasonality"})

    return quotes


def get_quotes_from_db(market="KC-057"):
    """
    Return array of quotes for send to front
    :param market: market for loading
    """
    quotes = (
        db.session.query(Quote.date, Quote.close, Quote.seasonality)
        .filter(Quote.market == market)
        .all()
    )

    quotes_for_send = list()
    for quote in quotes:
        quotes_for_send.append(
            {
                "date": quote.date.isoformat(),
                "close": quote.close,
                "seasonality": round(quote.seasonality * 5),
            }
        )

    return json.dumps(quotes_for_send)
