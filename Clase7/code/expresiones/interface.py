from abstract.expresion import Expresion
from symbols.env import Environment
from symbols.symbol import Symbol
from symbols.type import Type


class Interface(Expresion):
    def __init__(self, line, column, name, props):
        self.line = line
        self.column = column
        self.name = name
        self.props = props

    def resolver(self, env: Environment):
        symbol = Symbol(self.name, self.props, Type.INTERFACE)
        env.add_symbol(symbol)
