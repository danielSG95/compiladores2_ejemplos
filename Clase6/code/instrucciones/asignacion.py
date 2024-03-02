from abstract.instruccion import Instruccion
from symbols.env import Environment
from symbols.symbol import Symbol

class Asignacion(Instruccion):
    def __init__(self, line, col, name, expresion):
        self.line = line
        self.column = col
        self.name = name
        self.expresion = expresion

    def ejecuta(self, env:Environment):
        print('asignando valor')
        result = env.get_symbol(self.name)

        if result:
            #La variable existe
            valor = self.expresion.resolver(env) # el tipo resultante sea el mismo que el de la TS
            # verificar que se haya resuelto bien
            env.update_symbol(Symbol(self.name, valor.value, result.type, result.is_constant))
        else:
            print('Error la variable no ha sido declarada')