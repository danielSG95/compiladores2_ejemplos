import ply.lex as lex
import ply.yacc as yacc

from expresiones.literal import Literal
from symbols.type import Type

from expresiones.aritmetica import Aritmetica, AritmeticaOp
from expresiones.relacional import Relacional, RelacionalOp
from expresiones.logica import Logica, LogicaOp

# instrucciones
from instrucciones.declaracion import Declaracion
from instrucciones.print import Print
from instrucciones.asignacion import Asignacion

reservadas = {
    'console': 'CONSOLE',
    'log': 'LOG',
    'var': 'VAR',
    'const': 'CONST',
    'number': 'NUMBER',
    'string': 'STRING'
}

symbols = [
    'DOT',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COLON'
]

relational = [
    'MAYOR',
    'MENOR',
    'MAYORI',
    'MENORI',
    'DIFF',
    'IGUAL',  # ==
    'ASIG'  # =
]

logical = [
    'AND',
    'NOT',
    'OR'
]

arithmetic = [
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULE'
]

tokens = ['TNUMBER', 'TSTRING', 'ID']

tokens += list(reservadas.values()) + symbols + \
          relational + logical + arithmetic

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'%'
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COLON = r':'
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYORI = r'>='
t_MENORI = r'<='
t_AND = r'&&'
t_NOT = r'!'
t_OR = r'\|\|'
t_DIFF = r'!='
t_IGUAL = r'=='
t_ASIG = r'='

# reservadas
t_CONSOLE = r'console'
t_LOG = r'log'
t_VAR = r'var'
t_CONST = r'const'
t_NUMBER = r'number'
t_STRING = r'string'

# caracteres ignorados
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    # return t


def t_TNUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except:
        print('error inesperado en el lexico')
        t.value = -1
    return t


def t_TSTRING(t):
    r'\"(.+?)\"'
    try:
        t.value = str(t.value).replace('"', '')
    except:
        print('error')
        t.value = ''
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    try:
        t.type = reservadas.get(t.value, 'ID')
    except:
        print(f'Error reconocer el ID {t.value}')
    return t


def t_error(t):
    print(f'Error lexico {t.value}')
    t.lexer.skip(1)  # recuperacion del error


precedence = (('left', 'PLUS', 'MINUS'), ('left', 'TIMES',
                                          'DIVIDE', 'MODULE'), ('right', 'UMENOS'))


def p_init(p):
    """ init : instrucciones"""
    p[0] = p[1]


def p_instrucciones(p):
    """ instrucciones : instrucciones instruccion
    				| instruccion"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_instruccion(p):
    """ instruccion : instruccion_inline """
    p[0] = p[1]


def p_instruccion_inline(p):
    """ instruccion_inline : print
                          | declare
                          | asignacion """
    p[0] = p[1]


def p_print(p):
    """ print : CONSOLE DOT LOG LPAREN expresion_logica RPAREN SEMICOLON"""
    p[0] = Print(p.lineno, p.lexpos, p[5])



def p_declare(p):
    """ declare : tipo_declaracion ID COLON tipo_dato ASIG expresion_logica SEMICOLON"""
    p[0] = Declaracion(p.lineno, p.lexpos, p[2], p[4], p[6], p[1])

def p_asignacion(p):
    """ asignacion : ID ASIG expresion_logica SEMICOLON"""
    p[0] = Asignacion(p.lineno, p.lexpos, p[1], p[3])


def p_tipo_declaracion(p):
    """ tipo_declaracion : CONST
    					| VAR"""
    if p.slice[1].type == 'CONST':
        p[0] = True
    else:
        p[0] = False


def p_expresion_logica(p):
    """ expresion_logica : expresion_relacional AND expresion_relacional
                        | expresion_relacional OR expresion_relacional
                        | NOT expresion_relacional
                        | expresion_relacional"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Logica(p.lineno, p.lexpos, -1, p[2], LogicaOp.NOT)
    else:
        p[0] = Logica(p.lineno, p.lexpos, p[1], p[3], LogicaOp[p.slice[2].type])


def p_expresion_relacional(p):
    """ expresion_relacional : expresion_numerica MAYOR expresion_numerica
                            | expresion_numerica MENOR expresion_numerica
                            | expresion_numerica MAYORI expresion_numerica
                            | expresion_numerica MENORI expresion_numerica
                            | expresion_numerica IGUAL expresion_numerica
                            | expresion_numerica DIFF expresion_numerica
                            | expresion_numerica"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Relacional(p.lineno, p.lexpos, p[1], p[3], RelacionalOp[p.slice[2].type])


def p_expresion(p):
    """ expresion_numerica : MINUS expresion_numerica %prec UMENOS
    			| expresion_numerica PLUS expresion_numerica
    			| expresion_numerica MINUS expresion_numerica
				| expresion_numerica TIMES expresion_numerica
				| expresion_numerica DIVIDE expresion_numerica
				| expresion_numerica MODULE expresion_numerica
       		    | terminal"""
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = Aritmetica(p.lineno, p.lexpos, -1, p[2], AritmeticaOp.MINUS)
    else:
        p[0] = Aritmetica(p.lineno, p.lexpos, p[1], p[3], AritmeticaOp[p.slice[2].type])


def p_terminal(p):
    """ terminal : TNUMBER
    			| TSTRING
       		    | ID"""
    if p.slice[1].type == 'TSTRING':
        p[0] = Literal(p.lineno, p.lexpos, str(p[1]), Type.STRING)
    elif p.slice[1].type == 'TNUMBER':
        p[0] = Literal(p.lineno, p.lexpos, p[1], Type.NUMBER)
    else:
        p[0] = Literal(p.lineno, p.lexpos, p[1], Type.IDENTIFICADOR)


# var suma = 2 + 2
# var suma: number = 2 + 2
def p_tipo_dato(p):
    """ tipo_dato : STRING
                | NUMBER
                | empty"""
    if p.slice[1].type == 'STRING':
        p[0] = Type.STRING
    elif p.slice[1].type == 'NUMBER':
        p[0] = Type.NUMBER
    else:
        p[0] = Type.NULL


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        print(f'Error sintactico linea:{p.lineno}, col: {
        p.lexpos}: Token {p.value}')
    else:
        print('Error de sintaxis')


def parse(input):
    lexer = lex.lex()
    parser = yacc.yacc()
    return parser.parse(input, lexer=lexer)
