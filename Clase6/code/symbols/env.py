from symbols.symbol import Symbol

class Environment():
    def __init__(self, parent):
        self.parent = parent
        self._tabla_simbolos = {}

    def add_symbol(self, symbol: Symbol):
        if not self.find_symbol(symbol.id):
            self._tabla_simbolos[symbol.id] = symbol
        else:
            raise "La variable ya fue declarada"

    def update_symbol(self, symbol: Symbol):
        if self.find_symbol(symbol.id):
            self._tabla_simbolos[symbol.id] = symbol
        else:
            print('no se ha declarado')

    def get_symbol(self, id):
        if id in self._tabla_simbolos:
            return self._tabla_simbolos[id]
        else:
            return None

    def find_symbol(self, id):
        if id in self._tabla_simbolos:
            return True
        return False

    def get_variable(self, id):
        return self._find_variable(id, self)

    def _find_variable(self, id, padre):
        if padre == None:
            return None

        current = padre._tabla_simbolos
        for elemento in current:
            if elemento == id:
                return current[elemento]

        return self._find_variable(id, padre.parent)