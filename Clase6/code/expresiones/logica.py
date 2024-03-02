from abstract import expresion
from symbols.type import Type
from expresiones.literal import Literal
from enum import Enum



class Logica(expresion.Expresion):
    def __init__(self, line, col, left, right, op):
        self.line = line
        self.column = col
        self.left = left
        self.right = right
        self.op = op

    def resolver(self, env):
        left_result = self.left.resolver(env)
        right_result = self.right.resolver(env)

        print(left_result)

        if left_result.data_type != Type.BOOLEAN and right_result.data_type != Type.BOOLEAN:
            print('error semantico tipos incompatibles')
            return Literal(self.line, self.col, None, Type.ERR)

        if self.op == LogicaOp.AND:
            return Literal(self.line, self.column, (left_result.value and right_result.value), Type.BOOLEAN) #True | False
        elif self.op == LogicaOp.OR:
            return Literal(self.line, self.column, (left_result.value or right_result.value), Type.BOOLEAN)
        elif self.op == LogicaOp.NOT:
            return Literal(self.line, self.column, (not right_result.value), Type.BOOLEAN)




class LogicaOp(Enum):
    AND = 1
    NOT = 2
    OR = 3