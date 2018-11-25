import sys
sys.path.append("..")
import json
import ply.yacc as yacc
from lexAnalyzer import *
from models.MainClass import *
from models.Attribute import *
from models.Method import *
from models.ResponseClass import *

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
        resultado = "Error sintactico en Linea {} Posicion {} de Tipo {} cerca del Valor {}".format(str(t.lineno),str(t.lexpos),str(t.type),str(t.value))
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
        itemNotValid = 0
        for item in self.data.splitlines():
            if item:
                gram = parser.parse(item)
                if gram:
                    resultado_gramatica.append(str(gram))
            else:
                itemNotValid += 1

        #print("result: ", resultado_gramatica)
        return resultado_gramatica

    def getData(self):
        try:
            resultSyntactic = self.testSyntacticResult()
            isValid = True
            responseObj = ResponseClass()
            if len(resultSyntactic) > 0:
                for item in resultSyntactic:
                    if item == "True":
                        isValid = True
                    else:
                        isValid = False
                        break

                # If syntactic grammar is correct then get the token by lexical function
                if isValid:
                    lexerObj = Lexer
                    lexResult = lexerObj.testLexResult(self.data)
                    classObj = MainClass()
                    responseObj.success = True
                    responseObj.message = "La sintaxis es valida"
                    idx = 0
                    # Iterate all tokens and get the necessary token for the response
                    for token in lexResult:
                        # Get the class name on lex array
                        if token.type == "LLAIZQ":
                            classObj.name = lexResult[idx - 1].value
                        # Get the attribute information
                        if token.type == "PUNTOCOMA" and lexResult[idx - 1].type == "IDENTIFICADOR":
                            attrName = lexResult[idx - 1].value
                            attrType = lexResult[idx - 2].value
                            attrScope = lexResult[idx - 3].value
                            attrObj = Attribute(attrScope, attrType, attrName)
                            classObj.lstAttributes.append(attrObj.__dict__)

                        # Get the method information
                        if token.type == "PARIZQ" and lexResult[idx + 1].type == "PARDER":
                            methodName = lexResult[idx - 1].value
                            methodType = lexResult[idx - 2].value
                            methodScope = lexResult[idx - 3].value
                            methodObj = Method(methodScope, methodType, methodName)
                            classObj.lstMethods.append(methodObj.__dict__)

                        # To know when the class has finished and set the Class object on list
                        if token.type == "LLADER":
                            responseObj.lstClasses.append(classObj.__dict__)
                            classObj = MainClass()

                        idx += 1

                    # print(classObj.name)
                    # for attr in classObj.lstAttributes:
                    #     print(attr.__dict__)
                    # for method in classObj.lstMethods:
                    #     print(method.__dict__)
                else:
                    # Get all message error
                    resultSyntactic[:] = (value for value in resultSyntactic if value != "True")
                    responseObj.success = False
                    responseObj.message = "Error de sintaxis encontrado"
                    responseObj.lstSyntaxErros = resultSyntactic
            else:
                responseObj.success = False
                responseObj.message = "Ningun resultado que mostrar. No se ha encontrado ningun token valido."

        except Exception as exc:
            responseObj.success = False
            responseObj.message = "Error al obtener los datos: " + str(exc)

        return responseObj
        #print(responseObj.message)
            # print(len(result_grammar))
            # print(result_grammar[0])



if __name__ == '__main__':
    testFile = open("testGrammar.txt", "r")
    content = testFile.read()
    # print(content)
    objAnalyzer = Analyzer(content)
    responseObj = objAnalyzer.getData().__dict__
    print(json.dumps(responseObj))
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