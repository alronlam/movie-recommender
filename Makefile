.PHONY: help conda-env setup requirements
-include .env

conda-env:
	conda env create --prefix ./env -f environment.yml --no-default-packages

setup:
	pip install pip-tools==7.3.*
	pip-sync requirements.txt
	pre-commit install

requirements:
	pip-compile requirements.in -o requirements.txt -v
	pip-sync requirements.txt

dev:
	npm run dev &
	./env/bin/python3 manage.py runserver
	