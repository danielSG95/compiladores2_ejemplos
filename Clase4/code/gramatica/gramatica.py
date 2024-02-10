import ply.lex as lex
import ply.yacc as yacc

from nodo.nodo import Nodo 
from nodo.tipo_nodo import TipoNodo

reservadas = {
    'console': 'CONSOLE',
    'log': 'LOG',
    'var': 'VAR',
    'const': 'CONST',
}

# tokens = ('NUMBER', 'PARA', 'PARC',
#           'SUMA', 'LOG',
#           'MENOS', 'POR', 'DIV', 'SC',
#           'PUNTO', 'STRING', 'IGUAL', 'ID')
tokens = ['NUMBER', 'PARA', 'PARC',
          'SUMA','MENOS', 'POR', 'DIV', 'SC',
          'PUNTO', 'STRING', 'IGUAL', 'ID'] + list(reservadas.values())

# token
t_CONSOLE = r'console'
t_LOG = r'log'
t_VAR = r'var'
t_CONST = r'const'

t_PARA = r'\('
t_PARC = r'\)'
t_SUMA = r'\+'
t_POR = r'\*'
t_PUNTO = r'\.'
t_IGUAL = r'='

t_SC = r';'
t_MENOS = r'-'
t_DIV = r'/'

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f'error al parsear el valor: {t.value}')
        t.value = -1

    return t

def t_STRING(t):
    r'\"(.+?)\"'
    try:
        t.value = str(t.value)
    except ValueError:
        print(f'error al parsear el valor: {t.value}')
        t.value = '' 

    return t

def t_ID(t):
    r'[a-zA-Z]+' # warning no se esta comprobando palabras reservadas
    t.type = reservadas.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print(f'Error lexico {t.value}')
    t.lexer.skip(1) # recuperacion del error


precedence = (
        ('left', 'SUMA', 'MENOS'),
        ('left','POR', 'DIV'),
        ('right', 'UMENOS'),)


def p_instrucciones(p):
    '''instrucciones : instrucciones instruccion
                     | instruccion '''
    if len(p) == 2:
        n = Nodo(p.lineno(1), p.lexpos(0), TipoNodo.INSTRUCCION)
        n.add_hijo(p[1])
        p[0] = n
    else:
        n = Nodo(TipoNodo.INSTRUCCION)
        n.add_hijo(p[2])
        p[1].add_hijo(n)


def p_instruccion(p):
    '''instruccion : print
                   | declaracion'''
    p[0] = p[1]

def p_print(p):
    '''print : CONSOLE PUNTO LOG PARA expresion PARC SC'''
    p[0] = Nodo(p.lineno(1), p.lexpos(0), TipoNodo.PRINT)
    p[0].add_hijo(p[5])


def p_declaracion(p):
    '''declaracion : tipo_var ID IGUAL expresion SC'''
    p[0] = Nodo(p.lineno(1), p.lexpos(0), TipoNodo.VARIABLE, valor=p[2])
    p[0].add_hijo(p[4])

def p_tipo_var(p):
    '''tipo_var : CONST
                | VAR '''
    p[0] = Nodo(p.lineno(1), p.lexpos(0),TipoNodo.TERMINAL, valor=p[1] )


def p_expresion(p):
    '''expresion : MENOS expresion %prec UMENOS
                 | expresion SUMA expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIV expresion
                 | datos'''

    if len(p) == 2: #subimos datos
        p[0] = p[1]
    elif len(p) == 3: # subimos el -Number
        p[0] = Nodo(p.lineno(1), p.lexpos(0), TipoNodo.OPERADOR_UNARIO, valor=p[2])
    elif len(p) == 4:
        n = Nodo( p.lineno(1), p.lexpos(0), TipoNodo.OPERADOR_BINARIO, valor=p[22])
        n.add_hijo(p[1])
        n.add_hijo(p[3])
        p[0] = n

    #  + 
    #/  \
#   3    4


def p_datos(p):
    '''datos : NUMBER
             | STRING '''
    p[0] = Nodo(p.lineno(1), p.lexpos(0), TipoNodo.TERMINAL, valor=p[1]) 


def p_error(p):
    if p:
        print(f'Error sintactico linea:{p.lineno}, col: {p.lexpos}: Token {p.value}')
    else:
        print('Error de sintaxis')



def parse(input):
    lexer = lex.lex() #lexico
    parser = yacc.yacc(lexer) #sintactico

    print(input)
    result = parser.parse(input)
    return result
