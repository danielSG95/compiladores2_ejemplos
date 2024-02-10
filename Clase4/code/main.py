from gramatica import gramatica
import graphviz
def recorrer(dot, root):
    for hijo in root.hijos:
        print(f'{hijo.tipo_nodo} - {hijo.valor}')
        dot.node(str(id(hijo)), f'{hijo.tipo_nodo} - {hijo.valor}')
        dot.edge(str(id(root)), str(id(hijo)))
        recorrer(dot, hijo)

def generar_grafo(root):
    dot = graphviz.Digraph('ast')
    recorrer(dot, root)

    dot.render(directory='doctest-output').replace('\\', '/')

if __name__ == "__main__":
    input = 'console.log("text");'
    resultado = gramatica.parse(input)

    generar_grafo(resultado)
    
