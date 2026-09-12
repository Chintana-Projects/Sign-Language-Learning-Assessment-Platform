from locust import HttpUser, task, between

class SignSyncUser(HttpUser):

    wait_time = between(1, 3)

    @task
    def dashboard(self):
        self.client.get(
            "/assessment/report/15"
        )

    @task
    def history(self):
        self.client.get(
            "/assessment/history/15"
        )