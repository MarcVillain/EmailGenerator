PYTHON   = python3
BIN      = generate.py
TEMPLATE = template.eml
OUTPUT   = output

.PHONY: all install run debug format clean

all:
	make run

install:
	$(PYTHON) -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

run:
	$(PYTHON) $(BIN) --output $(OUTPUT)

debug:
	$(PYTHON) $(BIN) --debug --number 1 --output $(OUTPUT)

format:
	black *.py **/*.py

clean:
	$(RM) -rf $(OUTPUT)
