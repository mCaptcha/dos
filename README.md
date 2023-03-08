<div align="center" >

# DoS Demo: Comparing mCaptcha-protected endpoint performance against exposed endpoints with non-simulated, realistic load

**This demo uses a registration workflow that looks as real as
possible: password and password re-type confirmation followed by
password hashing and storing in DB**

</div>

## Requirements

1. mCaptcha server with a captcha configured. Please self-host an
   mCaptcha instance as the demo server is just that --- a demo server. See
   [here](https://github.com/mCaptcha/mCaptcha/blob/master/docs/DEPLOYMENT.md)
   for deployment instructions.

2. Python 3.10.4: might work on other versions but I tested it on this
   version

3. rustc: [`mCaptcha/pow_py`](https://github.com/mCaptcha/pow_py), the
   proof of work library used in mCaptcha(well, the Python bindings to
   it) is not published on pypi(still figuring out how to) so the user
   will have to compile from source

## Overview:

-   [server](./server/): a demo flask endpoint with two endpoints that do
    the exact same thing: process and register a user but differ in the
    fact the one of them(`/protected`) is protected by mCaptcha.

-   [unprotected](./unprotected): DoS Client written using
    [locust](https://locust.io) that launches an attack on the unprotected
    endpoint

-   [protected](./unprotected): DoS Client written using
    [locust](https://locust.io) that launches an attack on the rotected
    endpoint. It generates proof of work and solves the captcha on every
    request.

## Funding

### NLnet

<div align="center">
	<img
		height="150px"
		alt="NLnet NGIZero logo"
		src="./docs/third-party/NGIZero-green.hex.svg"
	/>
</div>

<br />

2023 development is funded through the [NGI0 Entrust
Fund](https://nlnet.nl/entrust), via [NLnet](https://nlnet.nl/). Please
see [here](https://nlnet.nl/project/mCaptcha/) for more details.
