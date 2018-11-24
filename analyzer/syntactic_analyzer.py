import ply.yacc as yacc
from lex_analyzer import *
# from lex_analyzer import analyzer

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('nonassoc','CLASS'),
    ('left', 'IDENTIFICADOR', 'LLAIZQ'),
)
nombres = {}

# sintactico de expresiones logicas
def p_class_syntax(t):
    '''
    expresion   :  CLASS IDENTIFICADOR LLAIZQ
                |  PUBLIC INT IDENTIFICADOR PUNTOCOMA
                |  PRIVATE INT IDENTIFICADOR PUNTOCOMA
                |  PROTECTED INT IDENTIFICADOR PUNTOCOMA
                |  PUBLIC STRING IDENTIFICADOR PUNTOCOMA
                |  PRIVATE STRING IDENTIFICADOR PUNTOCOMA
                |  PROTECTED STRING IDENTIFICADOR PUNTOCOMA
                |  PUBLIC BOOL IDENTIFICADOR PUNTOCOMA
                |  PRIVATE BOOL IDENTIFICADOR PUNTOCOMA
                |  PROTECTED BOOL IDENTIFICADOR PUNTOCOMA
                |  PUBLIC VOID IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PRIVATE VOID IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PROTECTED VOID IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PUBLIC INT IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PRIVATE INT IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PROTECTED INT IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PUBLIC STRING IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PRIVATE STRING IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PROTECTED STRING IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PUBLIC BOOL IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PRIVATE BOOL IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  PROTECTED BOOL IDENTIFICADOR PARIZQ PARDER PUNTOCOMA
                |  LLADER
    '''
    # print(t.__dict__)
    t[0] = True

def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintactico de tipo {} cerca del valor {}".format( str(t.type),str(t.value))
        #print(resultado)
    else:
        resultado = "Token No identificado"
        #print(resultado)
    resultado_gramatica.append(resultado)



# Instanciar el parser
parser = yacc.yacc()

class Analyzer:
    def __init__(self, data):
        self.data = data

    def testSyntacticResult(self):
        global resultado_gramatica
        resultado_gramatica.clear()

        for item in self.data.splitlines():
            if item:
                gram = parser.parse(item)
                if gram:
                    resultado_gramatica.append(str(gram))
            else:
                print("Item vacio")

        #print("result: ", resultado_gramatica)
        return resultado_gramatica

    def getData(self):
        result_grammar = self.testSyntacticResult()

        if len(result_grammar):
            print(len(result_grammar))
            print(result_grammar[0])


if __name__ == '__main__':
    testFile = open("testGrammar.txt", "r")
    content = testFile.read()
    print(content)
    objAnalyzer = Analyzer(content)
    objAnalyzer.getData()
    # while True:
    #     try:
    #         stringInput = input(' ingresa dato >>> ')
    #     except EOFError:
    #         continue
    #
    #     if not stringInput:
    #         continue

        # gram = parser.parse(s)
        # print("Resultado ", gram)
        #objAnalyzer = Analyzer(stringInput)
        #objAnalyzer.testSyntacticResult()
        #objAnalyzer.getData()