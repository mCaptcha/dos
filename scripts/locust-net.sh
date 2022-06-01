#!/bin/bash

docker run \
	-v tmp/unprotected/:/tmp/unprotected \
	-p 8001:8001 \
	-p 8089:8089 \
	-e MCAPTCHA_CAPTCHA_SITEKEY:MCAPTCHA_CAPTCHA_SITEKEY \
	mcaptcha/mcaptcha-locust-unprotected \
	--web-port 8089 \
	--master \
	--master-bind-port 8001 \
	--csv $(date +%s) --csv-full-history --html $(date +%s).html


docker run \
	--network=host \
	-e MCAPTCHA_CAPTCHA_SITEKEY:MCAPTCHA_CAPTCHA_SITEKEY \
	mcaptcha/mcaptcha-locust-unprotected \
	--worker \
	--master-port 8001

docker run \
	-v tmp/unprotected/:/tmp/unprotected \
	-p 8002:8002 \
	-p 8090:8090 \
	-e MCAPTCHA_CAPTCHA_SITEKEY:MCAPTCHA_CAPTCHA_SITEKEY \
	mcaptcha/mcaptcha-locust-unprotected \
	--master \
	--master-bind-port 8002 \
	--web-port 8090 \
	--csv $(date +%s) --csv-full-history --html $(date +%s).html


docker run \
	--network=host \
	-e MCAPTCHA_CAPTCHA_SITEKEY:MCAPTCHA_CAPTCHA_SITEKEY \
	mcaptcha/mcaptcha-locust-unprotected \
	--worker \
	--master-port 8002
