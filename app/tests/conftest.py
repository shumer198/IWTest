import pytest

from app.main import create_app
from app.models.models import Client, ClientParking, Parking
from app.models.models import db as _db


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()

        client = Client(id=1, name="name", surname="surname", credit_card="123123123")

        parking = Parking(
            id=1,
            address="asdasdas",
            opened=1,
            count_places=200,
            count_available_places=30,
        )

        client_parking = ClientParking(id=1, client_id=1, parking_id=1)

        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
