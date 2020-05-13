PYTHON   = python3
BIN      = generate.py
TEMPLATE = template.eml

.PHONY: all run debug format clean

all:
	make run

install:
	$(PYTHON) -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

run:
	$(PYTHON) $(BIN)

debug:
	$(PYTHON) $(BIN) --debug

format:
	black *.py **/*.py

clean:
	$(RM) -rf $(OUTPUT)
