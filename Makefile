.DEFAULT_GOAL := help

ENV_FILE = .env

ACTIVATE = . venv/bin/activate &&
ANSIBLE = $(ACTIVATE) ansible-playbook

include .env
export

COMPOSE = docker compose -f compose.yaml
ifeq (${USE_PROXY},true)
	COMPOSE += -f compose.proxy.yaml
endif

define usage
	@printf "\nUsage: make <command>\n"
	@grep -F -h "##" $(MAKEFILE_LIST) | grep -F -v grep -F | sed -e 's/\\$$//' | awk 'BEGIN {FS = ":*[[:alnum:] _]*##[[:space:]]*"}; \
	{ \
		if($$2 == "") \
			pass; \
		else if($$0 ~ /^#/) \
			printf "\n%s\n", $$2; \
		else if($$1 == "") \
			printf "     %-20s%s\n", "", $$2; \
		else \
			printf "\n    \033[1;33m%-20s\033[0m %s\n", $$1, $$2; \
	}'
endef

.git/hooks/pre-commit: .pre-commit-config.yaml
	@if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then \
		$(ACTIVATE) pre-commit install --hook-type pre-commit; \
		@touch $@; \
	fi

venv/.touchfile: requirements-dev.txt
	@test -d venv || python3 -m venv venv
	@$(ACTIVATE) pip install -U uv && uv pip install -Ur $<
	@touch $@
venv: .git/hooks/pre-commit venv/.touchfile

.PHONY: help
help: Makefile  ## Print this message
	@$(usage)

## Mail Server

.PHONY: provision
provision: venv  ## Provision the mail server
	@$(ANSIBLE) ./ansible/provision.yaml

## Development

.PHONY: up
up:  ## Start the mail container
	@$(COMPOSE) up -d --build

.PHONY: down
down:  ## Stop the mail container
	@$(COMPOSE) down --remove-orphans

.PHONY: sh
sh:  ## Start a shell in the mail container
	@$(COMPOSE) exec inbox bash

.PHONY: restart
restart: down up  ## Restart the mail container

## Development

.PHONY: check
check: venv  ## Check the code
	@$(ACTIVATE) pre-commit run --all-files
