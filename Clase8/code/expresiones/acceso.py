from abstract.expresion import Expresion
from symbols.env import Environment


class Acceso(Expresion):
    def __init__(self, line, column, id, prop):
        super().__init__(line, column)
        self.id = id
        self.prop = prop

    def resolver(self, env: Environment):
        variable = env.get_symbol(self.id)
        if variable is None:
            return None

        if self.prop in variable.value:
            return variable.value[self.prop]

        return None
