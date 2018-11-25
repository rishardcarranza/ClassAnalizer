import sys
sys.path.append("..")
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from compiladores.forms import area
from analyzer.syntacticAnalyzer import Analyzer
import unicodedata



def index(request):
    if request.method == 'POST':
        form = area(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        return HttpResponseRedirect('/contactos/gracias/')
    else:
        form = area()
        return render(request, 'index.html', {'form': form})

def procesar(request):
    if 'textarea' in request.GET and request.GET['textarea']:
        mensaje = request.GET['textarea']

        f=open ('parse.txt','w')
        f.write(mensaje)
        f.close()

        testFile = open("parse.txt", "r")
        content = testFile.read()

        analizador=Analyzer(content)
        object=analizador.getData()



        return render(request, 'index.html', {'estado':object.success, 'text':mensaje, 'clases':object.lstClasses, })
    else:
        return render(request, 'index.html',{'error':True})

