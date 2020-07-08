target:
	@$(MAKE) pr

dev:
	pipenv install

format:
	pipenv run isort -rc .
	pipenv run black src

lint: format
	pipenv run flake8

test:
	pipenv run pytest --cov

pr: lint test 

build:
	sam build
