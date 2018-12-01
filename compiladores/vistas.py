import sys
sys.path.append("..")
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from compiladores.forms import area
from analyzer.syntacticAnalyzer import Analyzer
import unicodedata

"""
Method to process the request with textarea content
"""
@csrf_exempt
def procesar(request):
    if 'txtClasses' in request.POST and request.POST['txtClasses']:
        mensaje = request.POST['txtClasses']
        writeFile = open('parse.in','w')
        writeFile.write(mensaje)
        writeFile.close()
        readFile = open("parse.in", "r")
        content = readFile.read()
        readFile.close()

        analizador=Analyzer(content)
        object=analizador.getData()
        return render(request, 'index.html', {'estado':object.success, 'text':mensaje, 'clases':object.lstClasses, 'errores':object.lstSyntaxErros })
    else:
        return render(request, 'index.html',{'error':True})

@csrf_exempt
def loadExample(request):
    readFile = open("example.in", "r")
    content = readFile.read()
    readFile.close()
    print(content)
    analyzer = Analyzer(content)
    object = analyzer.getData()

    # return render(request, 'index.html', {'estado':object.success, 'text':content, 'clases':object.lstClasses, 'errores':object.lstSyntaxErros })