import server


def test_server(client, monkeypatch, competitions, clubs):
    """
    Integration test for the server.py

    Args:
        client: Flask test client.
        monkeypatch: pytest monkeypatch fixture.
        competitions: Fixture providing mock competitions data.
        clubs: Fixture providing mock clubs data.
    """
    monkeypatch.setattr(server, "competitions", competitions)
    monkeypatch.setattr(server, "clubs", clubs)

    response_index = client.get("/")
    assert b"Please enter your secretary email to continue:" in response_index.data

    response_point_board = client.get("/displayboard")
    assert response_point_board.status_code == 200
    assert b"Club points display board" in response_point_board.data

    response_show_summary = client.post(
        "/showSummary", data={"email": clubs[0]["email"]}
    )
    assert response_show_summary.status_code == 200

    response_purchase_places = client.post(
        "/purchasePlaces",
        data={
            "club": clubs[0]["name"],
            "competition": competitions[2]["name"],
            "places": 1,
        },
    )
    assert b"Great, booking complete!" in response_purchase_places.data
    assert b"Number of places available: 19" in response_purchase_places.data

    response_logout = client.get("/logout")
    assert response_logout.status_code == 302  # redirected http code
