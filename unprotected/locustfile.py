from locust import HttpUser, between, task


class Unprotected(HttpUser):
    #    wait_time = between(5, 15)

    @task
    def unprotected(self):
        password = "fooobarasdfasdf"
        username = "realaravinth"
        data = {"username": username, "password": username, "confirm_password": username}
        self.client.post("/unprotected", data=data)
