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
	$(PYTHON) $(BIN) $(TEMPLATE) --output $(OUTPUT)

debug:
	$(PYTHON) --debug $(BIN) $(TEMPLATE) --output $(OUTPUT)

format:
	black *.py

clean:
	$(RM) -rf $(OUTPUT)
