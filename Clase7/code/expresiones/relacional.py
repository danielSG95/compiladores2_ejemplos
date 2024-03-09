from abstract import expresion
from expresiones.literal import Literal
from symbols.type import Type
from enum import Enum


class Relacional(expresion.Expresion):
    def __init__(self, line, col, left, right, op):
        self.line = line
        self.column = col
        self.left = left
        self.right = right
        self.op = op

    def resolver(self, env):
        izdo = self.left.resolver(env)
        dcho = self.right.resolver(env)

        if self.op == RelacionalOp.MAYOR:
            return Literal(self.line, self.column, (izdo.value > dcho.value), Type.BOOLEAN)



class RelacionalOp(Enum):
    MAYOR = 1
    MENOR = 2
    MAYORI = 3
    MENORI = 4
    DIFERENCIA = 5
    IGUAL = 6
