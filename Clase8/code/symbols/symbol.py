class Symbol:
    def __init__(self, id, valor, type, is_constant=False):
        self.id = id
        self.value = valor
        self.type = type
        self.is_constant = is_constant
