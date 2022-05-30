import pytest

from app.models.models import Client, Parking

from .factories import ClientFactory, ParkingFactory


@pytest.mark.factory_test
def test_create_user(app, db):
    client = ClientFactory()
    db.session.commit()
    assert client.id is not None
    assert len(db.session.query(Client).all()) == 2


@pytest.mark.factory_test
def test_create_parking(app, db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
    assert len(db.session.query(Parking).all()) == 2
