import random

import factory

from app.models.models import Client, Parking, db


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_card = random.choice([None, factory.Faker("credit_card_number")])
    car_number = factory.Faker("license_plate")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("street_address")
    opened = random.choice([True, False])
    count_places = random.randint(1, 1000)
    count_available_places = factory.LazyAttribute(
        lambda x: random.randrange(0, ParkingFactory.count_places)
    )
