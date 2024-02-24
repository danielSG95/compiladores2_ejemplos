from abstract import expresion
from enum import Enum


class Relacional(expresion.Expresion):
    def __init__(self, line, col, left, right, op):
        self.line = line
        self.col = col
        self.left = left
        self.right = right
        self.op = op

    def resolver(self, env):
        print('operacion relacional')


class RelacionalOp(Enum):
    MAYOR = 1
    MENOR = 2
    MAYORI = 3
    MENORI = 4
    DIFERENCIA = 5
    IGUAL = 6
