from abstract.instruccion import Instruccion
from instrucciones.retorno import Return
from symbols.env import Environment

class While(Instruccion):
    def __init__(self, line, column, condition, statements):
        super().__init__(line, column)
        self.condition = condition
        self.statements = statements

    def resolver(self, env):
        new_env = Environment(env)
        resultado = self.condition.resolver(env)

        if resultado is not None:
            while resultado.value:
                for statement in self.statements:
                    valor = statement.resolver(new_env)
                    if isinstance(statement, Return):
                        return valor
                resultado = self.condition.resolver(env)