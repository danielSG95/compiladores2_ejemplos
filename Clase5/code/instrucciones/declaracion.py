from abstract.instruccion import Instruccion
from symbols.env import Environment
from symbols.symbol import Symbol

class Declaracion(Instruccion):
    def __init__(self, line, col, name, type, expresion, is_constant=False):
        self.line = line
        self.column = col
        self.name = name
        self.type = type
        self.expresion = expresion
        self.is_constant = is_constant

    def ejecuta(self, env:Environment):
        expresion = self.expresion.resolver(env)
        try:
            if expresion:
                simbolo = Symbol(self.name, expresion.value, self.type, self.is_constant)
                env.add_symbol(simbolo)
        except:
            print('error al guardar la variable')
