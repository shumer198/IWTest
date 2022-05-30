import datetime
import logging
from typing import Any, Dict

from flask_sqlalchemy import SQLAlchemy
# from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import IntegrityError, NoResultFound

# from app.schemas.schemas import (
#     ClientParkingParametersSchema,
#     ClientSchema,
#     ParkingSchema,
#     ResponseClientSchema,
# )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db = SQLAlchemy()


class Quote(db.Model):
    __tablename__ = "quote"

    id = db.Column(db.Integer, db.Sequence("quote_id_seq"), primary_key=True)
    market = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open = db.Column(db.Float, nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    close = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("market", "date", name="unique_market_date"),
    )

    def __repr__(self):
        return f"Quotes {self.market} {self.date} {self.close}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def get_quotes_for_market(market: str):
    try:
        quotes = db.session.query(Quote).filter(Quote.market == market).all()
        print(quotes)
        return '200'
        # return ResponseClientSchema.from_orm(client).json()
    except NoResultFound as exc:
        logger.info(f"No Content. {exc}")
        return "No Content", 204
    # except ValidationError as exc:
    #     logger.info(f"Validation error {exc}")
    #     return "Internal server error", 500


# def add_new_client(client):
#     try:
#         client = ClientSchema(**client)
#         client = Client(**client.dict())
#         db.session.add(client)
#         db.session.commit()
#         return "Ok", 201
#     except ValidationError as exc:
#         logger.info(f"Validation error {exc}")
#         return "Internal server error", 500
