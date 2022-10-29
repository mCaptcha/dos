default: ## Run app
	. ./venv/bin/activate && maturin build

#coverage:
#	# rustup component add llvm-tools-preview is required
#	$(call test_interface)
#	@. ./venv/bin/activate && ./scripts/coverage.sh --coverage
#	@. ./venv/bin/activate && coverage xml && coverage html
#	@. ./venv/bin/activate && ./scripts/coverage.sh --coverage
#

env: ## Install all dependencies
	@-virtualenv venv
	. ./venv/bin/activate && pip install maturin
	. ./venv/bin/activate && cd ../pow_sha256-py/ && maturin build && pip install .
	. ./venv/bin/activate && pip install -r requirements.txt
#	. ./venv/bin/activate && pip install -e .
	#. ./venv/bin/activate && pip install '.[test]'

freeze: ## Freeze python dependencies
	@. ./venv/bin/activate && pip freeze > requirements.txt
	@-sed -i '/mcaptcha-pow-py.*/d' requirements.txt
	@-sed -i '/maturin.*/d' requirements.txt

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint: ## Run linter
	@./venv/bin/black protected/
	@./venv/bin/black unprotected/
	@./venv/bin/black server/src/

#test: ## Run tests
#	@. ./venv/bin/activate
#	$(call	test_pow_sha_256_py)

serve:
	. ./venv/bin/activate && FLASK_APP=server/src/app FLASK_ENV=development flask run
