from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    """
    Load testing class for the project endpoints.
    """
    @task
    def index(self):
        """
        Task to simulate a user accessing the index route.
        """
        self.client.get("/")

    @task
    def display_board(self):
        """
        Task to simulate a user accessing the displayboard route.
        """
        self.client.get("/displayboard")

    @task
    def show_summary(self):
        """
        Task to simulate a user accessing the showSummary route.
        """
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book(self):
        """
        Task to simulate a user accessing the book route.
        """
        self.client.get("/book/Winter%20Festival/Simply%20Lift")

    @task
    def purchase_places(self):
        """
        Task to simulate a user purchasing places.
        """
        self.client.post(
            "/purchasePlaces",
            data={"club": "Simply Lift", "competition": "Test Festival", "places": 1},
        )

    @task
    def logout(self):
        """
        Task to simulate a user logging out.
        """
        self.client.get("/logout")
