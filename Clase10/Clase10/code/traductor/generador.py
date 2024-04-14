from symbols.type import Type

class Generador():
    generator = None
    def __init__(self):
        self.header = ''
        self.data = ''
        self.text = '.text\n.globl main\nmain:\n'
        self.labelCounter = 1


    def get_instance(self):
        if Generador.generator is None:
            Generador.generator = Generador()
        return Generador.generator

    def declare_variable(self, name, value, data_type):
        if data_type == Type.NUMBER:
            self.declare_number(name, value)
        elif data_type == Type.STRING:
            self.declare_string(name, value)


    def declare_number(self, name, value):
        self.data += f'{name}: .word {value}\n'

    def declare_string(self, name, value):
        self.data += f'{name}: .asciz "{value}"\n'


    def print_number(self, value):
        self.text += f'lw a0, {value}' # cargamos una palabra porque asumimos que viene desde una variable
        self.text += f'li a7, 1\n'
        self.text += f'ecall\n'
        self.text += f'li, a0, 10\n'
        self.text += f'li a7, 11\n'
        self.text += 'ecall\n'


    def print_string(self, value, size):
        self.text += f'li a0, 1\n'
        self.text += f'la a1, {value}\n'
        self.text += f'li a2, {size}\n'
        self.text += f'li a7, 64\n'
        self.text += 'ecall\n'
        self.text += f'li a0, 10\n'
        self.text += f'li a7, 11\n'
        self.text += 'ecall\n'