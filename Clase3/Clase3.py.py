import ply.lex as lex
import ply.yacc as yacc

# 3 + 6 ( 2 3)n 

tokens = ('DIGIT', 'PARA', 'PARC', 'SUMA')

# token
t_PARA = r'\('
t_PARC = r'\)'
t_SUMA = r'\+'

t_ignore = ' \t'


def t_DIGIT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print(f'Error al intentar parsear el valor: {t.value}')
        t.value = -1
    return t


def t_error(t):
    print(f'Ha ocurrido un error lexico {t}')


def p_s(p):
    '''S : E'''
    p[0] = p[1]


def p_e(p):
    '''E : E SUMA F
         | F '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[3]


def p_f(p):
    '''F : PARA E PARC
         | DIGIT '''

    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2] 


def p_error(p):
    if p:
        print(f'Error sintactico linea:{p.lineno}, col: {p.lexpos}: Token {p.value}')
    else:
        print('Error de sintaxis')


if __name__ == "__main__":
    input_text = '3 + 6 + (2 + 3)'

    lexer = lex.lex() #lexico
    parser = yacc.yacc() #sintactico

    result = parser.parse(input_text)
    print(f'Resultado: {result}')
