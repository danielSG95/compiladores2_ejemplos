from abc import ABC, abstractclassmethod


class Instruccion(ABC):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    @classmethod
    def resolver(self, env): pass
