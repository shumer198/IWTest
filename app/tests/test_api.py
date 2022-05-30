import json

import pytest


def test_app_config(app):
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"


def test_get_client(client) -> None:
    resp = client.get("/clients/1")
    assert resp.status_code == 200


@pytest.mark.parametrize("route", ["/", "/clients", "/clients/1"])
def test_route_status(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client) -> None:
    client_data = {
        "name": "Y",
        "surname": "test surname",
        "credit_card": "1111111",
        "car_number": "55555555",
    }
    client_data = json.dumps(client_data)
    resp = client.post(
        "/clients",
        data=client_data,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    assert resp.status_code == 201


def test_create_parking(client) -> None:
    parking_data = {
        "address": "Truda str 16",
        "opened": "True",
        "count_places": "50",
        "count_available_places": "7",
    }
    parking_data = json.dumps(parking_data)
    resp = client.post(
        "/parkings",
        data=parking_data,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )

    assert resp.status_code == 201


@pytest.mark.parking
def test_add_client_parking(client) -> None:
    client_parking_data = {"client_id": 2, "parking_id": 1}

    client_parking_data = json.dumps(client_parking_data)
    resp = client.post(
        "/client_parkings",
        data=client_parking_data,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )

    assert resp.status_code == 201


@pytest.mark.xfail()
def test_client_already_parking(client) -> None:
    client_parking_data = {"client_id": 1, "parking_id": 1}
    client_parking_data = json.dumps(client_parking_data)
    resp = client.post(
        "/client_parkings",
        data=client_parking_data,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )

    assert resp.status_code == 201


@pytest.mark.parking
def test_del_client_parking(client) -> None:
    client_parking_data = {"client_id": 1, "parking_id": 1}

    client_parking_data = json.dumps(client_parking_data)
    resp = client.delete(
        "/client_parkings",
        data=client_parking_data,
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )

    assert resp.status_code == 202
