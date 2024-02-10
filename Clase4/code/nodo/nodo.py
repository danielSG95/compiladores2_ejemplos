
class Nodo():
    def __init__(self, linea, columna, tipo_nodo, valor='', data_type='' ) -> None:
        self.valor = valor
        self.linea = linea
        self.columna = columna
        self.tipo_nodo = tipo_nodo
        self.data_type = data_type
        self.hijos = []

    def add_hijo(self, hijo):
        self.hijos.append(hijo)
