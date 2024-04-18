import pytest
import server
from server import app


@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask application.

    Returns:
        FlaskClient: Test client for the Flask application.
    """
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def clubs(monkeypatch):
    """
    Fixture to provide mock data for clubs.

    Args:
        monkeypatch: pytest monkeypatch fixture.

    Returns:
        list: List of mock clubs data.
    """
    clubs = [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13",
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4",
        },
        {
            "name": "She Lifts",
            "email": "kate@shelifts.co.uk",
            "points": "12",
        },
    ]

    monkeypatch.setattr(server, "clubs", clubs)
    return clubs


@pytest.fixture
def competitions(monkeypatch):
    """
    Fixture to provide mock data for competitions.

    Args:
        monkeypatch: pytest monkeypatch fixture.

    Returns:
        list: List of mock competitions data.
    """
    competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
            },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
            },
        {
            "name": "Winter Festival",
            "date": "2024-10-24 09:30:00",
            "numberOfPlaces": "20",
            },
        {
            "name": "Test Festival",
            "date": "2024-08-31 14:00:00",
            "numberOfPlaces": "8"
            }
    ]

    monkeypatch.setattr(server, "competitions", competitions)
    return competitions
