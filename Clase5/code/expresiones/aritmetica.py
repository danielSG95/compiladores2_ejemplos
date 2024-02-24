from abstract import expresion
from expresiones.literal import Literal
from enum import Enum


class Aritmetica(expresion.Expresion):
    def __init__(self, line, col, left, right, op):
        self.line = line
        self.col = col
        self.left = left
        self.right = right
        self.op = op

    def resolver(self, env):
        left_op = self.left.resolver(env)
        right_op = self.right.resolver(env)

        # validar que se hayan resuelto correctamente

        if self.op == AritmeticaOp.PLUS:
            return Literal(self.line, self.col, left_op.value + right_op.value, left_op.data_type)
        elif self.op == AritmeticaOp.MINUS:
            return Literal(self.line, self.col, left_op.value - right_op.value, left_op.data_type)
        elif self.op == AritmeticaOp.TIMES:
            return Literal(self.line, self.col, left_op.value * right_op.value, left_op.data_type)
        elif self.op == AritmeticaOp.DIV:
            # puede dar error por divisiones entre 0
            return Literal(self.line, self.col, left_op.value / right_op.value, left_op.data_type)


class AritmeticaOp(Enum):
    PLUS = 1
    MINUS = 2
    TIMES = 3
    DIV = 4
    MOD = 5
