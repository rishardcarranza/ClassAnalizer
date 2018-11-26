from django import forms

class area(forms.Form):
    codigo=forms.CharField(widget=forms.Textarea, label='Ingrese el codigo')