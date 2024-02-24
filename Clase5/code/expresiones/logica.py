from abstract import expresion
from enum import Enum


class Logica(expresion.Expresion):
    def __init__(self, line, col, left, right, op):
        self.line = line
        self.col = col
        self.left = left
        self.right = right
        self.op = op

    def resolver(self, env):
        print('operacion relacional')


class LogicaOp(Enum):
    AND = 1
    NOT = 2
    OR = 3