PYTHON   = python3
BIN      = generate.py
TEMPLATE = template.eml
OUTPUT   = emails

.PHONY: all run debug format clean

all:
	make run

install:
	$(PYTHON) -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt

run:
	$(PYTHON) $(BIN) --template $(TEMPLATE) --output $(OUTPUT)

debug:
	$(PYTHON) $(BIN) --debug --template $(TEMPLATE) --output $(OUTPUT)

format:
	black *.py **/*.py

clean:
	$(RM) -rf $(OUTPUT)
