from abstract.instruccion import Instruccion
from symbols.env import Environment
from symbols.symbol import Symbol

class If(Instruccion):
    def __init__(self, line, column, bloqueSi, bloqueNo, rIf, expresion):
        self.line = line
        self.column = column
        self.bloqueSi = bloqueSi
        self.bloqueNo = bloqueNo
        self.rIf = rIf
        self.expresion = expresion

    def resolver(self, env):
        print('estoy en el bloque if')
        resultado = self.expresion.resolver(env)

        print(resultado)

        if resultado.value == True:
            # se crea el nuevo entorno y se ejecutan las instrucciones hijas del if
            inner_env = Environment(env)
            for instruccion in self.bloqueSi:
                instruccion.resolver(inner_env)
        else:
            # aqui debemos manejar la parte recursiv
            if self.rIf != None:
                self.rIf.resolver(env)

            print('el resultado es negativo...')
            if self.bloqueNo:
                inner_env = Environment(env)
                for instruccion in self.bloqueNo:
                    instruccion.resolver(inner_env)