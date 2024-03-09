from abstract.instruccion import Instruccion
from symbols.type import Type

class Return(Instruccion):
    def __init__(self, line, column, expression):
        self.line = line
        self.column = column
        self.expression = expression

    def resolver(self, env):
        if self.expression is not Type.NULL:
            resultado = self.expression.resolver(env)
            return resultado
        else:
            return Type.VOID
