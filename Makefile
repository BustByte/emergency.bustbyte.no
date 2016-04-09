PIP=$(shell which pip3)
PYTHON=$(shell which python3)
SRC_DIR=./src
TWISTED_SERVER=$(SRC_DIR)/webserver/server.py
MODULES=$(shell pwd)/$(SRC_DIR)

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

clean:
	-@find . -name '.DS_Store'   -delete
	-@find . -name '*.pyc' 		 -delete
	-@find . -name '__pycache__' -delete

.PHONY: install serve
