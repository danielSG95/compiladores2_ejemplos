from abstract.instruccion import Instruccion
from symbols.env import Environment
from symbols.symbol import Symbol
from symbols.type import Type
class Funcion(Instruccion):
    def __init__(self, line, column, name, params, t_retorno, l_instrucciones):
        self.line = line
        self.column = column
        self.name = name
        self.params = params
        self.t_retorno = t_retorno
        self.l_instrucciones = l_instrucciones

    def resolver(self, env:Environment):
        env.insert_function(Symbol(self.name, self, Type.FUNCTION))



# clase de apoyo, para encapsular los parametros.
class listParams():
    def __init__(self, value, data_type):
        self.value = value
        self.data_type = data_type