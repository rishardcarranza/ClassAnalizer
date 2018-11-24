import sys
sys.path.append("..")
import json
import ply.lex as lex
from models.Token import Token

# resultado del analisis
resultado_lexema = []

reservada = (
    # Palabras Reservadas
    'CLASS',
    'PUBLIC',
    'PRIVATE',
    'PROTECTED',
    'RETURN',
    'VOID',
    'INT',
    'BOOL',
    'STRING',
)
tokens = reservada + (
    'IDENTIFICADOR',
    'ENTERO',
    'ASIGNAR',

    # Symbolos
    'NUMERAL',
    'PARIZQ',
    'PARDER',
    'CORIZQ',
    'CORDER',
    'LLAIZQ',
    'LLADER',

    # Otros
    'PUNTOCOMA',
    'COMA',
    'COMDOB',
)

# Reglas de Expresiones Regulares para los tokens
t_ASIGNAR = r'='
t_PUNTOCOMA = ';'
t_COMA = r','
t_PARIZQ = r'\('
t_PARDER = r'\)'
t_CORIZQ = r'\['
t_CORDER = r'\]'
t_LLAIZQ = r'{'
t_LLADER = r'}'
t_COMDOB = r'\"'


def t_CLASS(t):
    r'class'
    return t


def t_PUBLIC(t):
    r'public'
    return t


def t_PRIVATE(t):
    r'private'
    return t


def t_PROTECTED(t):
    r'protected'
    return t


def t_RETURN(t):
    r'return'
    return t


def t_VOID(t):
    r'void'
    return t


def t_INT(t):
    r'int'
    return t

def t_BOOL(t):
    r'boolean'
    return t

def t_STRING(t):
    r'String'
    return t

def t_IDENTIFICADOR(t):
    r'\w+(_\d\w)*'
    return t


def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_comments(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    print("Comentario de bloque")


def t_comments_ONELine(t):
    r'\/\/(.)*\n'
    t.lexer.lineno += 1
    print("Comentario de una linea")


t_ignore = ' \t'

def t_error(t):
    global resultado_lexema
    status = "Token no valido en la Linea: {:4} Valor: {:16} Posicion: {:4}".format(str(t.lineno), str(t.value), str(t.lexpos))
    resultado_lexema.append(status)
    t.lexer.skip(1)


# Prueba de ingreso
class Lexer:
    def testLexResult(data):
        global resultado_lexema

        analyzer = lex.lex()
        analyzer.input(data)

        resultado_lexema.clear()
        while True:
            tok = analyzer.token()
            if not tok:
                break

            tokenObj = Token(tok.lineno, tok.type, tok.value, tok.lexpos)
            resultado_lexema.append(tokenObj.__dict__)

        return resultado_lexema


# instanciamos el analizador lexico
analyzer = lex.lex()

if __name__ == '__main__':
    response = {}
    response["success"] = True
    while True:
        stringInput = input("Ingrese cadena: ")
        if stringInput == "exit":
            break

        lexerObj = Lexer
        lexResult = lexerObj.testLexResult(stringInput)
        response["data"] = lexResult
        # for result in resultado_lexema:
        #     print(result.line, result.type, result.value, result.position)

    print(json.dumps(response))
