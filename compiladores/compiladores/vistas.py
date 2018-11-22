from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from compiladores.forms import area


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
        atributos=["nombres","apellidos", "jhovany"]
        return render(request, 'index.html', {'error': False, 'text':mensaje,'atribu': atributos, 'clase':'Persona' })
    else:
        return render(request, 'index.html',{'error':True})

