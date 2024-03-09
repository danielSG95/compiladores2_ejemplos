from abstract.instruccion import Instruccion
from symbols.type import Type


class Print(Instruccion):
    def __init__(self, line, col, expresion):
        self.line = line
        self.column = col
        self.expresion = expresion

    def resolver(self, env):
        value = self.expresion.resolver(env)

        if value is None or value.data_type == Type.NULL:
            print('Error la variable no se encuentra')
            return

        print(f'OLSCRIPT: {value.value} - {value.data_type}')
