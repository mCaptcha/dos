from locust import HttpUser, between, task


# import pow_sha256_py
# from pow_sha256_py import pow_py# import PowConfig, Work
# from pow_py import PowConfig, Work
import pow_py
import requests

# pow_sha256_py.pow_py.Config
class Unprotected(HttpUser):
    #    wait_time = between(5, 15)
    sitekey = "oupjLmu2Fs34JwlNKB1LsRAI1lfLx4So"

    @task
    def protected(self):
        key = {"key": self.sitekey}
        challenge_config = requests.post(
            "http://localhost:7000/api/v1/pow/config", json=key
        )
        challenge_config = challenge_config.json()

        #        print("working")
        config = pow_py.PoWConfig(challenge_config["salt"])
        work = config.work(
            challenge_config["string"], challenge_config["difficulty_factor"]
        )
        #        print(f"current difficulty factor: {challenge_config['difficulty_factor']}")
        #        print("proof generated")

        proof = {
            "key": self.sitekey,
            "nonce": work.nonce,
            "result": work.result,
            "string": challenge_config["string"],
        }
        resp = requests.post("http://localhost:7000/api/v1/pow/verify", json=proof)
        #        print(resp.text)
        #        print(resp.text)
        resp = resp.json()
        #        print(resp)
        token = resp["token"]

        #        print("token sent")
        data = {
            "username": "foo",
            "password": "foo",
            "confirm_password": "foo",
            "mcaptcha__token": token,
        }
        self.client.post("/protected", data=data)
