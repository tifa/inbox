include Make.defs
include .env

.PHONY: venv
venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || virtualenv venv
	. venv/bin/activate && pip install -Ur requirements.txt
	touch venv/touchfile

.PHONY: help
help: Makefile  # Print this message
	$(call usage)

.PHONY: build
build:  # Build the Docker image
	docker compose build prod

.PHONY: dev
dev:  # Enter dev mode
	docker compose build dev
	@echo "\nRun \`make\` to set up this server.\n"
	docker compose -v run --rm dev

.PHONY: docs
docs: venv  # Open docs
	. venv/bin/activate; cd docs && make html && open _build/html/index.html

.PHONY: restart
restart: stop start  # Restart the service

.PHONY: shell
shell:  # Enter shell
	docker compose exec prod bash

.PHONY: start
start:  # Start the service
	mkdir -p $(shell dirname $(SQLITE_DB_PATH)); touch $(SQLITE_DB_PATH)
	docker compose up -d prod
	docker compose exec prod make update

.PHONY: stop
stop:  # Stop the service
	docker compose rm prod -fs
