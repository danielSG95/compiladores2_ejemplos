from abstract.instruccion import Instruccion
from symbols.env import Environment
from symbols.symbol import Symbol
from symbols.type import Type
from expresiones.literal import Literal
from expresiones.aritmetica import Aritmetica
from traductor.generador import Generador


class Declaracion(Instruccion):
    def __init__(self, line, col, name, type, expresion, is_constant=False):
        self.line = line
        self.column = col
        self.name = name
        self.type = type
        self.expresion = expresion
        self.is_constant = is_constant

    def resolver(self, env: Environment):
        generador = Generador().get_instance()
        if isinstance(self.expresion, Literal):
            generador.declare_variable(self.name, self.expresion.value, self.type)
        elif isinstance(self.expresion, Aritmetica):
            generador.declare_variable(self.name, 0, self.type)
        expresion = self.expresion.resolver(env)
        try:
            if not expresion:
                print('error al resolver')
                return None
            if expresion.data_type == Type.PROP:
                # recuperar la definicion de la interfaz
                interface_schema = env.get_symbol(self.type.value)
                if not interface_schema:
                    print('El tipo al que hace referencia no existe')
                    return None

                if set(interface_schema.value.keys()) != set(expresion.value.keys()):
                    print(f'Faltan algunas propiedades para el tipo {self.type.value} {interface_schema.value.keys()}')
                    return None

                # aqui se sabe que se cumplen las propiedades, no sabemos si los tipos son los indicados

                for key, value in expresion.value.items():
                    if interface_schema.value[key] != value.data_type:
                        print('error los tipos no coinciden')
                        return None

                self.type = Type.INTERFACE

            simbolo = Symbol(self.name, expresion.value, self.type, self.is_constant)
            env.add_symbol(simbolo)
        except:
            print('error al guardar la variable')
