from abstract.instruccion import Instruccion
from symbols.env import Environment
from symbols.type import Type
from instrucciones.funcion import Funcion
from instrucciones.declaracion import Declaracion
from expresiones.literal import Literal
from instrucciones.retorno import Return


class Llamada(Instruccion):
    def __init__(self, line, column, name, largs):
        self.line = line
        self.column = column
        self.name = name
        self.largs = largs

    def resolver(self, env: Environment):
        symbol = env.find_function(self.name)
        if symbol is not None:
            new_env = Environment(env)
            function: Funcion = symbol.value
            if self.largs is not Type.NULL or function.params is not Type.NULL:
                if isinstance(self.largs, Type) is not isinstance(function.params, Type):
                    print('Error, falta de parametros')
                    return None
                if len(self.largs) != len(function.params):
                    print('la lista de parametros no coincide')
                    return None  # retornar un error aqui

                # Ahora se debe validar que todos los parametros proporcionados tenga el mismo tipo

                for i in range(len(function.params)):
                    if self.largs[i].data_type is not function.params[i].data_type:
                        print('Error los tipos de parametros no coinciden')
                        return None

                # ahora corresponde declarar los argumentos en el nuevo environment
                for i in range(len(function.params)):
                    temporal_literal = Literal(self.line, self.column, self.largs[i].value, self.largs[i].data_type)
                    temporal_declaration = Declaracion(self.line, self.column, function.params[i].value.value,
                                                       function.params[i].data_type, temporal_literal)

                    temporal_declaration.resolver(new_env)

            # ahora ejecuto, no importando si hay o no argumentos.

            for instruccion in function.l_instrucciones:
                result = instruccion.resolver(new_env)
                if function.t_retorno is not Type.VOID:
                    if isinstance(instruccion, Return):
                        if result.data_type is not function.t_retorno:
                            print('error, el tipo de retorno no coincide con el definido en la funcion')
                            return None
                        return result
                else:
                    if isinstance(instruccion, Return):
                        return None # Deberian de manejar mejor esto y valuar los otros casos
            # print(result)
