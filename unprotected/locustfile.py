from locust import HttpUser, between, task


class Unprotected(HttpUser):
    #    wait_time = between(5, 15)

    @task
    def unprotected(self):
        data = {"username": "foo", "password": "foo", "confirm_password": "foo"}
        self.client.post("/unprotected", data=data)
