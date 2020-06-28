Email Generator
===

This little script can let you generate random emails with ease.

# Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Run

```bash
python3 ./generate.py --help
```

# Scenarios

You can also load scenarios with the `--load` option. The format is the following:

```
emails:                     # List of emails to generate
- amount: 2                 # Amount of messages to exchange
  attachments:              # List of files to attach to each email
  - ["filename"]            # List of file names.
  NAME:                     # NAME must be in all caps
    attribute1: value       # attributes must be in all lowercase
    attribute2: value
  NAME:                     # If the NAME field is a list, it will
  - attribute1: value       # be iterated over, one value per email
    attribute2: ~           # You can use a ~ caracter to represent
  - attribute1: value       # an automatically generated value
```

Note that any missing field will be filled with a random value that will be used for the entire conversation.

Example that outputs three emails, with Person A exchanging with Person B, the subject is "Test" and the first and second messages respectively have "Test" and "Hello" as a body attribute value:

```
emails:
- amount: 3
  FROM:
    first: Person
    last: A
  TO:
    first: Person
    last: B
  SUBJECT:
    subject: Test
  MESSAGE:
  - body: Test
  - body: Hello
```

# Bibliography

* [rfc5322 (Internet Message Format)](https://tools.ietf.org/html/rfc5322)
* [rfc2046 (MIME Part two : Media Types)](https://tools.ietf.org/html/rfc2046)
* [rfc2183 (The Content-Disposition Header Field)](https://tools.ietf.org/html/rfc2183)
* [EML File Format](https://wiki.fileformat.com/email/eml/)

# Authors

* Marc Villain <marc.villain@epita.fr>
