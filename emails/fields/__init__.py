from abc import ABC


class Field(ABC):
    def __init__(self, fields):
        self.fields = fields
