from abc import ABC


class Field(ABC):
    def __init__(self, email):
        self.email = email
