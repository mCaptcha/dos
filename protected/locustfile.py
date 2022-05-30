import os

from locust import FastHttpUser, between, task
import mcaptcha_pow_py
import requests


password = "fooobarasdfasdf"
username = "realaravinth"

class Unprotected(FastHttpUser):
    wait_time = between(5, 15)
    sitekey = os.getenv("MCAPTCHA_CAPTCHA_SITEKEY")

    @task
    def protected(self):
        key = {"key": self.sitekey}
        challenge_config = requests.post(
            "http://localhost:7000/api/v1/pow/config", json=key
        )
        challenge_config = challenge_config.json()

        config = mcaptcha_pow_py.PoWConfig(challenge_config["salt"])
        pow_string  = challenge_config["string"]
        pow_difficulty_factor = challenge_config["difficulty_factor"]

        work = config.work(pow_string, pow_difficulty_factor)
        proof = {
            "key": self.sitekey,
            "nonce": work.nonce,
            "result": work.result,
            "string": challenge_config["string"],
        }
        resp = requests.post("http://localhost:7000/api/v1/pow/verify", json=proof)
        resp = resp.json()
        token = resp["token"]

        data = {
                "username": username,
                "password": username,
                "confirm_password": username,
                "mcaptcha__token": token,
        }
        response = self.client.post("/protected", data=data)
        print(pow_difficulty_factor)
