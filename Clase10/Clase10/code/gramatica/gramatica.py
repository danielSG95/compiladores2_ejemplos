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
from instrucciones.If import If

from instrucciones.funcion import Funcion, listParams
from instrucciones.llamada import Llamada
from instrucciones.retorno import Return
from expresiones.interface import Interface
from expresiones.acceso import Acceso

from instrucciones.while_inst import While

reservadas = {
    'console': 'CONSOLE',
    'log': 'LOG',
    'var': 'VAR',
    'const': 'CONST',
    'number': 'NUMBER',
    'string': 'STRING',
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'else': 'ELSE',
    'boolean': 'BOOLEAN',
    'while': 'WHILE',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'interface': 'INTERFACE'
}

symbols = [
    'DOT',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COLON',
    'LLAVE_A',
    'LLAVE_C',
    'COMA'
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
t_LLAVE_A = r'\{'
t_LLAVE_C = r'\}'
t_COMA = r','

# reservadas
t_CONSOLE = r'console'
t_LOG = r'log'
t_VAR = r'var'
t_CONST = r'const'
t_NUMBER = r'number'
t_STRING = r'string'
t_TRUE = r'true'
t_FALSE = r'false'
t_IF = r'if'
t_ELSE = r'else'
t_BOOLEAN = r'boolean'
t_WHILE = r'while'
t_FUNCTION = r'function'
t_RETURN = r'return'
r_INTERFACE = r'interface'

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
    """ init : instrucciones """
    p[0] = p[1]


# def p_linterface(p):
#     """ linterface : linterface interface_definition
#                     | interface_definition """
#     if len(p) == 2:
#         p[0] = [p[1]]
#     else:
#         p[1].append(p[2])
#         p[0] = p[1]


def p_instrucciones(p):
    """ instrucciones : instrucciones instruccion
    				| instruccion"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[2])
        p[0] = p[1]


def p_instruccion(p):
    """ instruccion : instruccion_inline
                    | instruccion_bloque
                    | interface_definition """
    p[0] = p[1]

def p_interface_definition(p):
    """ interface_definition : INTERFACE ID LLAVE_A interface_props SEMICOLON LLAVE_C"""
    p[0] = Interface(p.lineno, p.lexpos, p[2], p[4])

def p_interface_props(p):
    """ interface_props : interface_props SEMICOLON ID COLON tipo_dato
                        | ID COLON tipo_dato"""
    if len(p) == 4:
        p[0] = {p[1]: p[3]}
    else:
        p[1][p[3]] = p[5]
        p[0] = p[1]


def p_instruccion_inline(p):
    """ instruccion_inline : print
                          | declare
                          | asignacion
                          | llamada SEMICOLON
                          | retorno """
    p[0] = p[1]


def p_retorno(p):
    """ retorno : RETURN expresion_logica SEMICOLON
                | RETURN SEMICOLON"""
    if len(p) == 3:
        p[0] = Return(p.lineno, p.lexpos, Type.NULL)
    else:
        p[0] = Return(p.lineno, p.lexpos, p[2])


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

def p_instruccion_bloque(p):
    """ instruccion_bloque : instruccion_if
                            | instruccion_while
                            | declaracion_funcion"""
    p[0] = p[1]


def p_instruccion_if(p):
    """ instruccion_if : IF LPAREN expresion_logica RPAREN ifAux
                        | IF LPAREN expresion_logica RPAREN ifAux ELSE instruccion_if
                        | IF LPAREN expresion_logica RPAREN ifAux ELSE ifAux"""
    if len(p) == 6:
        p[0] = If(p.lineno, p.lexpos, p[5], None, None, p[3])
    elif len(p) == 8:
        print(p.slice[7].type)
        if p.slice[7].type == 'ifAux':
            p[0] = If(p.lineno, p.lexpos, p[5], p[7], None, p[3])
        else:
            p[0] = If(p.lineno, p.lexpos, p[5], None, p[7], p[3])
# if() {}
# if () {} else if () {} else if () {}
# if () {} else {}

def p_ifAux(p):
    """ ifAux : LLAVE_A instrucciones LLAVE_C"""
    p[0] = p[2]


def p_while(p):
    """ instruccion_while : WHILE LPAREN expresion_logica RPAREN LLAVE_A instrucciones LLAVE_C"""
    p[0] = While(p.lineno, p.lexpos, p[3], p[6])

def p_declaracion_funcion(p):
    """  declaracion_funcion : FUNCTION ID LPAREN params RPAREN fretorno LLAVE_A instrucciones LLAVE_C """
    p[0] = Funcion(p.lineno, p.lexpos, p[2], p[4], p[6], p[8])


def p_params(p):
    """ params : lparams
                | empty """
    if p.slice[1].type == 'lparams':
        p[0] = p[1]
    else:
        p[0] = Type.NULL

def p_lparams(p):
    """ lparams : lparams COMA param
                | param """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]


def p_param(p):
    """ param : expresion_logica COLON tipo_dato """
    p[0] = listParams(p[1], p[3])



def p_fretorno(p):
    """ fretorno : COLON tipo_dato
                | empty """
    if p.slice[1].type == 'empty':
        p[0] = Type.VOID
    else:
        p[0] = p[2]


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
    			| TRUE
    			| FALSE
       		    | ID
       		    | llamada
       		    | LLAVE_A lvalues LLAVE_C
       		    | ID DOT ID"""
    if p.slice[1].type == 'TSTRING':
        p[0] = Literal(p.lineno, p.lexpos, str(p[1]), Type.STRING)
    elif p.slice[1].type == 'TNUMBER':
        p[0] = Literal(p.lineno, p.lexpos, p[1], Type.NUMBER)
    elif p.slice[1].type == 'TRUE' or (p.slice[1].type == 'FALSE'):
        p[0] = Literal(p.lineno, p.lexpos, p[1], Type.BOOLEAN)
    elif p.slice[1].type == 'llamada':
        p[0] = Literal(p.lineno, p.lexpos, p[1], Type.FUNCTION)
    elif p.slice[1].type == 'ID':
        if len(p) == 2:
            p[0] = Literal(p.lineno, p.lexpos, p[1], Type.IDENTIFICADOR)
        else:
            p[0] = Acceso(p.lineno, p.lexpos, p[1], p[3])
    else:
        p[0] = Literal(p.lineno, p.lexpos, p[2], Type.PROP)

def p_lvalues(p):
    """ lvalues : lvalues COMA ID COLON expresion_logica
                | ID COLON expresion_logica"""
    if len(p) == 4:
        p[0] = {p[1]: p[3]}
    else:
        p[1][p[3]] = p[5]
        p[0] = p[1]

def p_llamada(p):
    """ llamada : ID LPAREN args RPAREN"""
    p[0] = Llamada(p.lineno, p.lexpos, p[1], p[3])

def p_args(p):
    """ args : lexpresiones
            | empty """
    if p.slice[1].type == 'lexpresiones':
        p[0] = p[1]
    else:
        p[0] = Type.NULL

def p_lexpresiones(p):
    """ lexpresiones : lexpresiones COMA expresion_logica
                    | expresion_logica """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[1].append(p[3])
        p[0] = p[1]

# var suma = 2 + 2
# var suma: number = 2 + 2
def p_tipo_dato(p):
    """ tipo_dato : STRING
                | NUMBER
                | BOOLEAN
                | ID
                | empty"""
    if p.slice[1].type == 'STRING':
        p[0] = Type.STRING
    elif p.slice[1].type == 'NUMBER':
        p[0] = Type.NUMBER
    elif p.slice[1].type == 'BOOLEAN':
        p[0] = Type.BOOLEAN
    elif p.slice[1].type == 'ID':
        p[0] = Literal(p.lineno, p.lexpos, p[1], Type.IDENTIFICADOR)
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
