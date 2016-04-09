PIP=$(shell which pip3)
PYTHON=$(shell which python3)
SRC_DIR=./src
TWISTED_SERVER=$(SRC_DIR)/webserver/server.py
MODULES=$(shell pwd)/$(SRC_DIR)
DATABASE_DIR=$(SRC_DIR)/database
DATABASE_NAME=fake-db.db
DATABASE_FILE=$(DATABASE_DIR)/$(DATABASE_NAME)
TRANSFER_SH=https://transfer.sh

install:
	@$(PIP) install -r requirements.txt

twisted: export PYTHONPATH=$(MODULES)
twisted: export PYTHONDONTWRITEBYTECODE="false"
twisted:
	$(PYTHON) $(TWISTED_SERVER)

serve: export PYTHONPATH=$(MODULES)
serve: export PYTHONDONTWRITEBYTECODE="false"
serve: twisted clean

flask:
	@$(PYTHON) $(TWISTER_SERVER)

download-database:
	@curl $(TRANSFER_SH)/$(key)/$(DATABASE_NAME) --output $(DATABASE_FILE)

upload-database:
	@curl --upload-file $(DATABASE_FILE) $(TRANSFER_SH)/$(DATABASE_NAME)

clean:
	-@find . -name '.DS_Store'   -delete
	-@find . -name '*.pyc' 		 -delete
	-@find . -name '__pycache__' -delete

.PHONY: install serve download-database
