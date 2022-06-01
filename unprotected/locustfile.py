from locust import FastHttpUser, between, task

password = "fooobarasdfasdf"
username = "realaravinth"


class Unprotected(FastHttpUser):
    #    wait_time = between(5, 15)

    @task
    def unprotected(self):
        data = {
            "username": username,
            "password": username,
            "confirm_password": username,
        }
        self.client.post("/unprotected", data=data)
