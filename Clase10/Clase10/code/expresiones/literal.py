from abstract.expresion import Expresion
from symbols.env import Environment
from symbols.type import Type

class Literal(Expresion):
    def __init__(self, line, column, value, data_type):
        self.line = line
        self.column = column
        self.value = value
        self.data_type = data_type

    def resolver(self, env:Environment):
        salida = Literal(self.line, self.column, self.value, self.data_type)
        if self.data_type == Type.STRING:
            salida.value = str(self.value)
            # self.value = str(self.value)
        elif self.data_type == Type.NUMBER:
            # self.value = int(self.value)
            salida.value = int(self.value)
        elif self.data_type == Type.IDENTIFICADOR:
            value = env.get_variable(self.value)
            if value:
                # self.value = value.value
                salida.value = value.value
                if value.type == Type.INTERFACE:
                    # self.value = "\n".join(f"{clave}: {valor.value}" for clave, valor in value.value.items())
                    salida.value = "\n".join(f"{clave}: {valor.value}" for clave, valor in value.value.items())
                # self.data_type = value.type
                salida.data_type = value.type
            else:
                # registrar el error
                # self.value = 'null'
                salida.value = 'null'
                salida.data_type = Type.NULL
                # self.data_type = Type.NULL
        elif self.data_type == Type.FUNCTION:
            resultado = self.value.resolver(env)
            # self.value = resultado.value
            salida.value = resultado.value
            salida.data_type = resultado.data_type
            # self.data_type = resultado.data_type
        elif self.data_type == Type.BOOLEAN:
            # self.value = self.value == 'true' #True
            # self.data_type = Type.BOOLEAN # no es necesario
            salida.value = self.value == 'true'
            salida.data_type = Type.BOOLEAN

        return salida # retornamos el litera, solo hacemos casteos necesarios.