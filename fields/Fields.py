class Fields:
    def __init__(self):
        self.values = {}

    def add(self, name, type):
        self.values[name] = type(self)

    def get(self, name):
        return self.values[name]

    def as_str_dict(self):
        d = dict()
        for key, value in self.values.items():
            d[key] = str(value)
        return d
