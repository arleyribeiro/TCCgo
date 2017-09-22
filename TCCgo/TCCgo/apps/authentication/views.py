from django.shortcuts import render

# Create your views here.
# VIEW DE TESTE
def index(request):
    return render(request, 'index.html');
