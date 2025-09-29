SHELL=/usr/bin/env bash

# Conda environment name and Python version
ENV_NAME = dra
PYTHON_VERSION = 3.11

# Default goal
.DEFAULT_GOAL := help

# 🛠️ Create Conda environment
.PHONY: create
create:
	conda create -y -n $(ENV_NAME) python=$(PYTHON_VERSION)

# 🛠️ Show activation command for Conda environment
.PHONY: activate
activate:
	@echo "Run: conda activate $(ENV_NAME)"

# 🛠️ Remove Conda environment
.PHONY: clean
clean:
	conda remove -y --name $(ENV_NAME) --all

# 🛠️ Install dependencies using Poetry
.PHONY: install
install:
	@echo "Installing dependencies"
	conda run -n $(ENV_NAME) pip install poetry
	conda run -n $(ENV_NAME) pip install 'markitdown[all]'
	conda run -n $(ENV_NAME) pip install "browser-use[memory]"==0.1.48

	@echo install playwright
	conda run -n $(ENV_NAME) pip install playwright
	conda run -n $(ENV_NAME) playwright install chromium --with-deps --no-shell

	@echo install dependencies
	conda run -n $(ENV_NAME) poetry install

install-requirements:
	@echo "Installing dependencies"
	conda run -n $(ENV_NAME) pip install poetry
	conda run -n $(ENV_NAME) pip install 'markitdown[all]'
	conda run -n $(ENV_NAME) pip install "browser-use[memory]"==0.1.48

	@echo install playwright
	conda run -n $(ENV_NAME) pip install playwright
	conda run -n $(ENV_NAME) playwright install chromium --with-deps --no-shell

	@echo install dependencies
	conda run -n $(ENV_NAME) pip install -r requirements.txt

# 🛠️ Update dependencies using Poetry
.PHONY: update
update:
	poetry update

# 🛠️ Show available Makefile commands
.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  make create      - Create Conda environment and install Poetry"
	@echo "  make activate    - Show activation command"
	@echo "  make clean       - Remove Conda environment"
	@echo "  make install     - Install dependencies using Poetry"
	@echo "  make update      - Update dependencies using Poetry"
