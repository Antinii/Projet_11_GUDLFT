import server
from unittest.mock import patch


def test_index(client):
    """
    Test for the index route.

    Args:
        client: Flask test client.
    """
    response = client.get("/")
    assert b"Please enter your secretary email to continue" in response.data


def test_logout(client):
    """
    Test for the logout route.

    Args:
        client: Flask test client.
    """
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    response_logout = client.get("/logout")
    assert response_logout.status_code == 302  # redirected http code


class TestShowSummary:
    """
    Test suite for the showSummary route.
    """
    def test_show_summary_valid_email(self, client):
        """
        Test for valid email input in showSummary route.
        """
        response = client.post("/showSummary", data={"email": "john@simplylift.co"})
        assert response.status_code == 200

    def test_show_summary_invalid_email(self, client):
        """
        Test for invalid email input in showSummary route.
        """
        response = client.post("/showSummary", data={"email": "user@test.com"})
        assert response.status_code == 200
        assert b"Email not found, please try again." in response.data

    def test_outdated_competition(self, monkeypatch, clubs, client, competitions):
        """
        Test for outdated competitions in showSummary route.

        Args:
            monkeypatch: pytest monkeypatch fixture.
            clubs: Fixture providing mock clubs data.
            client: Flask test client.
            competitions: Fixture providing mock competitions data.
        """
        monkeypatch.setattr(server, "competitions", competitions)
        club = clubs[0]
        response = client.post(
            "/showSummary",
            data={
                "email": club["email"],
            },
        )
        assert (
            'href="/book/Winter%20Festival' in response.data.decode()
        )  # upcoming competition
        assert (
            'href="/book/Test%20Festival' in response.data.decode()
        )  # upcoming competition
        assert (
            'href="/book/Spring%20Festival' not in response.data.decode()
        )  # outdated competition
        assert (
            'href="/book/Fall%20Classic' not in response.data.decode()
        )  # outdated competition


class TestBook:
    """
    Test suite for the book route.
    """
    def test_valid_booking(self, client):
        """
        Test for valid booking in book route.
        """
        response = client.get("/book/Winter Festival/Simply Lift")
        assert b"How many places?" in response.data

    def test_invalid_booking(self, client):
        """
        Test for invalid booking in book route.
        """
        response = client.get("/book/No Festival/Simply Lift")
        assert b"Something went wrong, please try again" in response.data


class TestPurchasePlaces:
    """
    Test suite for the purchasePlaces route.
    """
    def test_valid_purchase(self, client, clubs, competitions):
        """
        Test for valid purchase in purchasePlaces route.

        Args:
            client: Flask test client.
            clubs: Fixture providing mock clubs data.
            competitions: Fixture providing mock competitions data.
        """
        competition_name = competitions[2]["name"]  # competition 3 has 8 places
        club_name = clubs[0]["name"]  # club 1 only has 13 balance points
        places_to_book = 5
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club_name,
                "competition": competition_name,
                "places": places_to_book,
            },
        )
        assert b"Great, booking complete!" in response.data
        assert b"Number of places available: 15" in response.data

    def test_invalid_purchase_not_enough_points(self, client, clubs, competitions):
        """
        Test for invalid purchase because club has not enough points to book.
        """
        competition_name = competitions[2]["name"]
        club_name = clubs[1]["name"]  # club 2 only has 4 balance points
        places_to_book = 5
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club_name,
                "competition": competition_name,
                "places": places_to_book,
            },
        )
        assert b"Your point balance is not enough." in response.data
        assert b"Points available: 4" in response.data

    def test_invalid_purchase_not_enough_places(self, client, clubs, competitions):
        """
        Test for invalid purchase because competition has not enough places available.
        """
        competition_name = competitions[3]["name"]  # competition 4 has 8 places
        club_name = clubs[2]["name"]  # club 3 has 12 balance points
        places_to_book = 10
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club_name,
                "competition": competition_name,
                "places": places_to_book,
            },
        )
        assert (
            b"Not enough places available for the quantity you requested."
            in response.data
        )

    def test_invalid_purchase_invalid_value(self, client, clubs, competitions):
        """
        Test to verify the correct positive value of the places.
        """
        competition_name = competitions[1][
            "name"
        ]  # competition 2 has 3 places left after test_valid_purchase
        club_name = clubs[2]["name"]  # club 3 has 12 balance points
        places_to_book = -2
        response = client.post(
            "/purchasePlaces",
            data={
                "club": club_name,
                "competition": competition_name,
                "places": places_to_book,
            },
        )
        assert b"Incorrect value." in response.data

    def test_booking_over_limit(self, client, clubs, competitions):
        """
        Test for decline booking if the value of places is more then 12.
        """
        competition = competitions[2]["name"]
        club = clubs[0]["name"]
        places_to_book = 13
        response = client.post(
            "/purchasePlaces",
            data={"club": club, "competition": competition, "places": places_to_book},
        )
        assert response.status_code == 200
        assert b"Sorry! You can&#39;t book more then" in response.data


class TestDisplayBoard:
    """
    Test suite for the display_board route.
    """
    def test_display_board(self, client):
        """
        Test for the display_board route.
        """
        mock_clubs = [
            {'name': 'Club 1', 'points': 100},
            {'name': 'Club 2', 'points': 80},
            {'name': 'Club 3', 'points': 120}
        ]

        with patch('server.clubs', mock_clubs):
            response = client.get('/displayboard')
            assert response.status_code == 200
            assert b'Club 1' in response.data
            assert b'100' in response.data
            assert b'Club 2' in response.data
            assert b'80' in response.data
            assert b'Club 3' in response.data
            assert b'120' in response.data
