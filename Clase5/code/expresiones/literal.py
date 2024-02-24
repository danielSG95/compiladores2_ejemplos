from abstract.expresion import Expresion
from symbols.env import Environment
from symbols.type import Type

class Literal(Expresion):
    def __init__(self, line, column, value, data_type):
        self.line = line
        self.column = column
        self.value = value
        self.data_type = data_type

    def resolver(self, env:Environment):
        if self.data_type == Type.STRING:
            self.value = str(self.value)
        elif self.data_type == Type.NUMBER:
            self.value = int(self.value)
        elif self.data_type == Type.IDENTIFICADOR:
            value = env.get_symbol(self.value)
            if value:
                self.value = value.value
                self.data_type = value.type
            else:
                # registrar el error
                self.value = 'null'
                self.data_type = Type.NULL
        return self